# Added for TexttoMotion (2026): DeepMimic imitation with style targets set from text (not part of upstream MimicKit).
import math

import torch

import anim.motion_lib as motion_lib
import envs.deepmimic_env as deepmimic_env
from util.logger import Logger
import util.torch_util as torch_util


class TextRewardEnv(deepmimic_env.DeepMimicEnv):
    """DeepMimic tracking whose targets and terms are scaled versions of the (unchanged) reference.

    Optional env_config["text_reward"] entries:
      arm_swing: {scale}
          The arm joints (shoulders, elbows) are tracked against the reference rotation at
          the same time with its offset from the clip's mean arm pose multiplied by scale:
          the arms keep swinging like the reference, only wider. The scaled pose replaces
          the reference inside the DeepMimic terms (joint rotation, joint velocity, and the
          hand key positions from forward kinematics), so the arms are held as firmly as in
          plain DeepMimic. A separate arm term with the arm tracking switched off was too
          weak: the arms drifted 35-45 degrees from their target.
      foot_lift: {w, scale, k}
          Added term. Foot height above the reference's lowest foot height
          -> scale * reference clearance at the same time (squared error, both feet).
          The same foot heights replace the reference's in the DeepMimic key-position
          term. Looser errors were tried and dropped: penalising only a foot that is too
          low let the feet overshoot, and tolerating a foot that follows up to 0.1 s
          late made both feet step lower.
      upright: {w, scale, k}
          Added term. Tilt of the pelvis->head line from vertical -> scale * reference tilt.
      speed: {scale}
          The pelvis has to cover scale times the reference's ground distance in the same
          time. The reference's root path is stretched by scale from where the episode
          started, and its ground velocity is multiplied by scale; the DeepMimic root
          terms, the fall check and the target observations all use this path (an added
          speed term alone would fight the root position term, and the episode ends once
          the character is 1 m away from the reference). The walking rhythm is unchanged,
          so the step length changes: the thigh swing and the feet's forward reach are
          scaled as well, like the arms. Without that the speed is still met, but the leg
          targets contradict it and the whole pose is tracked less closely (elbows 12
          degrees off instead of 6 at scale 1.25).
      cadence: {scale}
          The clip is read scale times as fast: the target at time t is the reference at
          scale * t, so the character takes scale times as many steps per minute with the
          same step length. The target velocities (root, joints) are multiplied by scale,
          and the target observations look scale times as far ahead in the clip. Together
          with speed the ground speed is speed * cadence times the reference's.
      swing: {body: scale, ...}
          arm_swing for any joint: the joint of the named body is tracked against the
          reference rotation with its offset from the clip's mean rotation multiplied by
          scale (torso: 5 = the trunk rocks five times as far from its mean pose).
      pose: {body: [x, y, z], ...}
          The joint of the named body is tracked against the reference rotation turned by
          a constant rotation: degrees about the parent body's forward, left and up axes
          (an exp map). The motion stays, its mean pose moves (torso: [0, 20, 0] = the
          trunk bent 20 degrees forward; a shoulder: [0, -85, 0] = that arm held forward).
      crouch: {angle}
          Both thighs are turned forward by angle (deg) and both knees bent by twice the
          angle, which lowers the pelvis and keeps it over the feet. The ankles are set so
          that the feet keep the reference's orientation.
      bounce: {angle}
          The pelvis rises and falls further: in every frame the legs are bent as by crouch,
          by angle (deg) times how far the reference pelvis is below its highest point in the
          clip (0 at the top, 1 at the bottom). The low points of the gait sink deeper, the high
          points stay, and the feet stay on the ground as with crouch (2026-11-11).
      foot_pitch: {angle}
          Both feet are tipped about their own lateral axis by angle (deg), + toes down: the
          character walks on its toes (- on its heels). The pelvis height target rises by as
          much as the lowest edge of the soles (toe or heel) would leave the reference's height,
          so the tipped feet stand on the floor instead of in it. Applied after crouch, whose
          ankles keep the reference's foot orientation, so it holds on bent legs too (2026-11-12).
      weave: {amplitude}
          The reference's path swings sideways: its root and bodies are moved to the left of the
          clip's direction of travel (start to end of the clip, so that the pelvis's own yaw in
          every step does not shake the offset) by amplitude (m) times sin(2 pi t / WEAVE_PERIOD_S),
          t the time in the clip, and
          its ground velocity gets the rate of that offset. The root terms, the fall check and
          the target observations all use this path, as with speed; the clip's own motion and
          facing are kept, so the character walks a wavy line, stepping sideways (a drunk's
          weave, a zigzag) (2026-11-12).
      swing, pose and crouch change targets inside the DeepMimic terms like arm_swing:
      joint rotation, joint velocity (swing) and the key positions from forward kinematics.
      If they change a leg, the pelvis height target moves by as much as the lower foot
      would leave the reference's height, so the feet stay on the ground.
      swing_unit: {clip file}
          Swing and arm_swing scales above 1 add motion in units of this clip's motion
          (the walk): a joint swings 1 + (scale - 1) * min(1, unit amplitude / clip amplitude)
          times as far from its mean, amplitude = RMS angle from the mean over one cycle.
          The same scale then adds about as much motion in every clip (torso 5 on the walk
          clip itself stays 5; on the run, whose trunk already moves 3.6 times as much, it
          becomes 2.1). Scales of 1 or less keep that fraction of the clip's own motion.
      pose_unit: {clip file}
          A pose offset of an arm joint is measured from this clip's mean arm pose (the walk's
          hanging arms) instead of the clip's own, as seen in the heading frame: the upper arms
          also take back the difference between the two clips' mean trunk orientations, so
          their mean direction in the heading frame is the unit clip's plus the offset. The
          arm's motion stays around it. "Arms 85 degrees forward" then points the arms forward
          in every clip; measured from the run's bent, rotated arms the same offset spread them
          forward and outward, and measured from the walk's arms in the trunk frame alone they
          pointed down by the run's forward lean. Trunk, head and leg offsets stay relative to
          the clip's own posture (lean more or less than the action itself does).
      style: {w, k}
          Added term. The bodies whose joint the style changes (swing, pose, crouch) against
          their targets, both turned into the character's heading frame: the weighted mean of
          the squared angles, with the DeepMimic joint weights. Inside the DeepMimic terms a
          changed joint costs little (a 10 degree trunk offset left undone loses 1.3% of the
          reward on the kick clip), so on demanding clips the policy did half of it; here the posture the
          viewer sees is scored directly, and a trunk offset cannot be undone by tilting the
          pelvis the other way.
      The speed and cadence scales (_speed_scale, _cadence_scale) and the pose changes
      (_swing_scale, _pose_offset, _crouch_angle) are kept per environment so that
      viewers can run policies trained with different numbers in one simulation.
    Added terms are scored on a ladder of three sharpness values,
      kernel(err) = mean(exp(-k_far * err), exp(-sqrt(k_far * k) * err), exp(-k * err)),
    gentle K_FAR for a learning signal far from the target, sharp k for precision near it.
    The default k = "auto" is 1 / gap, where gap is the mean error of following the plain
    reference, floored by K_FLOOR (ordinary tracking noise).
    track_w weights the DeepMimic reward; observations do not change. The reward is
      r = (track_w * r_track + sum_i w_i * kernel_i(err_i)) / (track_w + sum_i w_i)
    Without text_reward the env is plain DeepMimic.
    """

    STYLE_TERMS = ("arm_swing", "foot_lift", "upright", "speed", "cadence", "swing", "pose", "crouch", "bounce", "swing_unit",
                   "pose_unit", "style")
    ADDED_TERMS = ("foot_lift", "upright")
    ARM_BODIES = ("right_upper_arm", "right_lower_arm", "left_upper_arm", "left_lower_arm")
    THIGH_BODIES = ("right_thigh", "left_thigh")
    SHIN_BODIES = ("right_shin", "left_shin")
    FOOT_BODIES = ("right_foot", "left_foot")
    FOOT_SOLE = ((0.1335, 0.0, -0.05), (-0.0435, 0.0, -0.05))  # toe and heel edges of the sole (humanoid.xml foot box)
    WEAVE_PERIOD_S = 3.0  # clip seconds of one full sideways swing of the path (about six walking steps)
    # Tracking-noise error per added term: (3 cm)^2 x 2 feet, (1 deg)^2, (3 deg)^2.
    K_FLOOR = {"foot_lift": 1.8e-3, "upright": 3e-4, "style": 2.7e-3}
    # Far-field sharpness: a 22 cm or 13 deg error scores exp(-1).
    K_FAR = {"foot_lift": 20.0, "upright": 20.0, "style": 20.0}

    def __init__(self, env_config, engine_config, num_envs, device, visualize, record_video=False):
        text_reward = env_config.get("text_reward") or {}
        self._track_w = float(text_reward.get("track_w", 1.0))
        self._arm_scale = float((text_reward.get("arm_swing") or {}).get("scale", 1.0))
        swing = dict(text_reward.get("swing") or {})
        pose = dict(text_reward.get("pose") or {})
        crouch = float((text_reward.get("crouch") or {}).get("angle", 0.0))
        bounce = float((text_reward.get("bounce") or {}).get("angle", 0.0))
        foot_pitch = float((text_reward.get("foot_pitch") or {}).get("angle", 0.0))
        self._style = {}
        for name in self.ADDED_TERMS:
            if (name in text_reward):
                term = {"w": 0.1, "scale": 1.0, "k": "auto", **text_reward[name]}
                self._style[name] = {"w": float(term["w"]), "scale": float(term["scale"]), "k": term["k"]}
        self._text_reward_ready = False  # the parent constructor already computes rewards
        speed = text_reward.get("speed") or {}
        self._speed_scale = torch.full([num_envs], float(speed.get("scale", 1.0)), device=device, dtype=torch.float)
        cadence = text_reward.get("cadence") or {}
        self._cadence_scale = torch.full([num_envs], float(cadence.get("scale", 1.0)), device=device, dtype=torch.float)
        self._path_start_xy = torch.zeros([num_envs, 2], device=device, dtype=torch.float)
        weave = float((text_reward.get("weave") or {}).get("amplitude", 0.0))
        self._weave_amp = torch.full([num_envs], weave, device=device, dtype=torch.float)
        self._weave_heading = 0.0  # the parent constructor already resets; the clip's direction is set once it is loaded
        self._obs_env_ids = None
        self._pose_unit_file = text_reward.get("pose_unit")
        self._pose_anchor = None  # [J, 4] unit mean * clip mean^-1 on the arm joints (pose_unit), identity elsewhere
        self._pose_lean = None  # [J, 4] clip trunk^-1 * unit trunk (heading frame) on the upper arms, identity elsewhere

        super().__init__(env_config=env_config, engine_config=engine_config,
                         num_envs=num_envs, device=device, visualize=visualize,
                         record_video=record_video)

        kin_char_model = self._kin_char_model
        body_names = kin_char_model.get_body_names()
        arm_body_ids = [body_names.index(name) for name in self.ARM_BODIES]
        # joint rotations exclude the root, so joint index = body index - 1
        self._arm_joint_ids = torch.tensor([body_id - 1 for body_id in arm_body_ids],
                                           device=self._device, dtype=torch.long)
        thigh_body_ids = [body_names.index(name) for name in self.THIGH_BODIES]
        self._thigh_joint_ids = torch.tensor([body_id - 1 for body_id in thigh_body_ids],
                                             device=self._device, dtype=torch.long)
        self._thigh_dof_ids = torch.tensor(
            [dof for body_id in thigh_body_ids
             for dof in range(kin_char_model.get_joint_dof_idx(body_id),
                              kin_char_model.get_joint_dof_idx(body_id) + kin_char_model.get_joint_dof_dim(body_id))],
            device=self._device, dtype=torch.long)
        self._hand_ids = self._build_body_ids_tensor(["right_hand", "left_hand"])
        self._foot_ids = self._build_body_ids_tensor(list(self.FOOT_BODIES))
        self._shin_ids = self._build_body_ids_tensor(list(self.SHIN_BODIES))
        num_joints = kin_char_model.get_num_joints() - 1
        self._leg_joint_ids = torch.cat([self._thigh_joint_ids, self._shin_ids - 1, self._foot_ids - 1])
        self._dof_joint_ids = torch.zeros(kin_char_model.get_dof_size(), device=self._device, dtype=torch.long)
        for body_id in range(1, num_joints + 1):
            dof_idx = kin_char_model.get_joint_dof_idx(body_id)
            self._dof_joint_ids[dof_idx:dof_idx + kin_char_model.get_joint_dof_dim(body_id)] = body_id - 1
        self._swing_scale = torch.ones([num_envs, num_joints], device=self._device, dtype=torch.float)
        self._swing_scale[:, self._arm_joint_ids] = self._arm_scale
        for name, scale in swing.items():
            self._swing_scale[:, body_names.index(name) - 1] = float(scale)
        self._pose_offset = torch.zeros([num_envs, num_joints, 4], device=self._device, dtype=torch.float)
        self._pose_offset[..., 3] = 1.0
        for name, angles in pose.items():
            exp_map = torch.tensor([angles], device=self._device, dtype=torch.float) * (math.pi / 180.0)
            self._pose_offset[:, body_names.index(name) - 1, :] = torch_util.exp_map_to_quat(exp_map)
        self._crouch_angle = torch.full([num_envs], crouch * math.pi / 180.0, device=self._device, dtype=torch.float)
        self._bounce_angle = torch.full([num_envs], bounce * math.pi / 180.0, device=self._device, dtype=torch.float)
        self._foot_pitch = torch.full([num_envs], foot_pitch * math.pi / 180.0, device=self._device, dtype=torch.float)
        Logger.print("text_reward swing: {}  pose: {}  crouch: {:.1f} deg".format(swing, pose, crouch)
                     + ("  bounce: {:.1f} deg".format(bounce) if bounce else "")
                     + ("  foot_pitch: {:.1f} deg".format(foot_pitch) if foot_pitch else ""))
        self._leg_joint_mask = torch.zeros(num_joints, device=self._device, dtype=torch.bool)
        self._leg_joint_mask[self._leg_joint_ids] = True
        self._foot_joint_mask = torch.zeros(num_joints, device=self._device, dtype=torch.bool)
        self._foot_joint_mask[self._foot_ids - 1] = True
        self._swing_gain = self._calc_swing_gain(text_reward.get("swing_unit"))
        style = text_reward.get("style") or {}
        style_joint_w = self._style_joint_w(self._swing_scale, self._pose_offset, self._crouch_angle + self._bounce_angle,
                                            self._foot_pitch)
        if (float(style.get("w", 0.0)) > 0.0 and bool(torch.any(style_joint_w > 0.0))):
            self._style["style"] = {"w": float(style["w"]), "scale": 1.0, "k": style.get("k", "auto")}
        self._head_id = self._build_body_ids_tensor(["head"])[0]
        ends = torch.zeros(2, dtype=torch.long, device=self._device)
        times = torch.stack([torch.zeros((), device=self._device), self._motion_lib.get_motion_length(ends[:1])[0]])
        travel = self._motion_lib.calc_motion_frame(ends, times)[0]
        self._weave_heading = float(torch.atan2(travel[1, 1] - travel[0, 1], travel[1, 0] - travel[0, 0]))
        self._calc_ref_stats()
        self._text_reward_ready = True
        return

    def _calc_ref_stats(self, num_samples=240):
        """Constants taken from one cycle of the first reference clip, and the auto sharpness."""
        motion_ids = torch.zeros(num_samples, dtype=torch.long, device=self._device)
        length = float(self._motion_lib.get_motion_length(motion_ids[:1])[0])
        times = torch.arange(num_samples, device=self._device, dtype=torch.float) * (length / num_samples)
        root_pos, root_rot, _, _, joint_rot, _ = self._motion_lib.calc_motion_frame(motion_ids, times)
        body_pos, body_rot = self._kin_char_model.forward_kinematics(root_pos, root_rot, joint_rot)

        self._foot_ground_h = body_pos[:, self._foot_ids, 2].min(dim=0).values
        self._root_h_hi, self._root_h_lo = float(root_pos[:, 2].max()), float(root_pos[:, 2].min())
        self._joint_mean_rot = calc_mean_quat(joint_rot)
        if (self._pose_unit_file):
            self._pose_anchor, self._pose_lean = self._calc_pose_anchor(self._pose_unit_file)
        self._arm_mean_rot = self._joint_mean_rot[self._arm_joint_ids]
        self._thigh_mean_rot = self._joint_mean_rot[self._thigh_joint_ids]
        Logger.print("text_reward arm_swing: scale={:.3f}".format(self._arm_scale))
        Logger.print("text_reward speed: scale={:.3f}".format(float(self._speed_scale[0])))
        Logger.print("text_reward cadence: scale={:.3f}".format(float(self._cadence_scale[0])))

        ref = (root_pos, body_pos)
        for name, term in self._style.items():
            if (term["k"] == "auto"):
                if (name == "style"):
                    gap = self._calc_style_gap(root_pos, root_rot, joint_rot, body_rot)
                else:
                    gap = float(self._style_error(name, term["scale"], ref, ref).mean())
                term["k"] = 1.0 / max(gap, self.K_FLOOR[name])
            else:
                term["k"] = float(term["k"])
            Logger.print("text_reward {:s}: w={:.3f} scale={:.3f} k={:.3f} k_far={:.3f}".format(
                name, term["w"], term["scale"], term["k"], self.K_FAR[name]))
        return

    def _calc_swing_gain(self, unit_file):
        """Gain [J] of swing scales above 1 (see swing_unit): min(1, unit amplitude / clip amplitude), 1 without a unit."""
        num_joints = self._kin_char_model.get_num_joints() - 1
        if (not unit_file):
            return torch.ones(num_joints, device=self._device, dtype=torch.float)
        unit_lib = motion_lib.MotionLib(motion_file=unit_file, kin_char_model=self._kin_char_model, device=self._device)
        unit_amp = self._calc_joint_amplitude(unit_lib)
        clip_amp = self._calc_joint_amplitude(self._motion_lib)
        gain = torch.where(clip_amp > 1e-3, torch.clamp(unit_amp / torch.clamp(clip_amp, min=1e-3), max=1.0),
                           torch.ones_like(clip_amp))
        Logger.print("text_reward swing_unit: {}  gain: {}".format(
            unit_file, " ".join("{:.2f}".format(g) for g in gain.tolist())))
        return gain

    def _calc_pose_anchor(self, unit_file, num_samples=240):
        """Rotations [J, 4] of pose_unit, identity on the other joints: the arm anchors (unit mean * clip
        mean^-1 on the arm joints) and the lean of the upper arms (clip trunk^-1 * unit trunk, the mean
        chest rotations in the heading frame)."""
        motion_ids = torch.zeros(num_samples, dtype=torch.long, device=self._device)
        length = float(self._motion_lib.get_motion_length(motion_ids[:1])[0])
        times = torch.arange(num_samples, device=self._device, dtype=torch.float) * (length / num_samples)
        root_pos, root_rot, _, _, joint_rot, _ = self._motion_lib.calc_motion_frame(motion_ids, times)
        _, body_rot = self._kin_char_model.forward_kinematics(root_pos, root_rot, joint_rot)
        unit_lib = motion_lib.MotionLib(motion_file=unit_file, kin_char_model=self._kin_char_model, device=self._device)
        unit_times = times * (float(unit_lib.get_motion_length(motion_ids[:1])[0]) / length)
        unit_root_pos, unit_root_rot, _, _, unit_rot, _ = unit_lib.calc_motion_frame(motion_ids, unit_times)
        _, unit_body_rot = self._kin_char_model.forward_kinematics(unit_root_pos, unit_root_rot, unit_rot)
        anchor = torch_util.quat_mul(calc_mean_quat(unit_rot), torch_util.quat_conjugate(calc_mean_quat(joint_rot)))
        chest = self._kin_char_model.get_body_names().index("torso")
        trunk = calc_mean_quat(heading_frame(root_rot, body_rot[:, chest:chest + 1, :]))
        unit_trunk = calc_mean_quat(heading_frame(unit_root_rot, unit_body_rot[:, chest:chest + 1, :]))
        lean = torch_util.quat_mul(torch_util.quat_conjugate(trunk), unit_trunk).expand(anchor.shape)
        identity = torch.zeros_like(anchor)
        identity[:, 3] = 1.0
        arms = torch.zeros_like(anchor[:, 0], dtype=torch.bool)
        arms[self._arm_joint_ids] = True
        upper_arms = torch.zeros_like(arms)
        upper_arms[self._arm_joint_ids[[0, 2]]] = True
        Logger.print("text_reward pose_unit: {}  arm anchors (deg): {}  trunk difference (deg): {:.1f}".format(
            unit_file, " ".join("{:.1f}".format(a) for a in (
                torch_util.quat_to_exp_map(anchor[self._arm_joint_ids]).norm(dim=-1) * 180.0 / math.pi).tolist()),
            float(torch_util.quat_to_exp_map(lean[:1]).norm(dim=-1)[0]) * 180.0 / math.pi))
        return torch.where(arms.unsqueeze(-1), anchor, identity), torch.where(upper_arms.unsqueeze(-1), lean, identity)

    def _calc_joint_amplitude(self, lib, num_samples=240):
        """RMS angle [J] of each joint's rotation from its mean rotation over one cycle of the first clip of lib."""
        motion_ids = torch.zeros(num_samples, dtype=torch.long, device=self._device)
        length = float(lib.get_motion_length(motion_ids[:1])[0])
        times = torch.arange(num_samples, device=self._device, dtype=torch.float) * (length / num_samples)
        joint_rot = lib.calc_motion_frame(motion_ids, times)[4]
        mean = calc_mean_quat(joint_rot).unsqueeze(0).expand(joint_rot.shape)
        angle = torch_util.quat_diff_angle(joint_rot, mean)
        return torch.sqrt(torch.mean(angle * angle, dim=0))

    def _effective_swing(self, swing_scale):
        """Swing scales [N, J] as applied to the clip (see swing_unit)."""
        gain = self._swing_gain.unsqueeze(0)
        return torch.where(swing_scale > 1.0, 1.0 + (swing_scale - 1.0) * gain, swing_scale)

    def _style_joint_w(self, swing_scale, pose_offset, crouch_angle, foot_pitch=None):
        """Weight [N, J] of each joint whose target the style changes (its DeepMimic joint weight), 0 elsewhere."""
        changed = (self._effective_swing(swing_scale) != 1.0) | (pose_offset[..., 3] != 1.0)
        changed = changed | ((crouch_angle != 0.0).unsqueeze(-1) & self._leg_joint_mask.unsqueeze(0))
        if (foot_pitch is not None):
            changed = changed | ((foot_pitch != 0.0).unsqueeze(-1) & self._foot_joint_mask.unsqueeze(0))
        return torch.where(changed, self._joint_err_w.unsqueeze(0), torch.zeros_like(swing_scale))

    def _calc_style_gap(self, root_pos, root_rot, joint_rot, body_rot):
        """Mean style error of the plain reference frames given, styled like the first environment."""
        num_frames = joint_rot.shape[0]
        swing = self._swing_scale[:1].expand(num_frames, -1)
        pose = self._pose_offset[:1].expand(num_frames, -1, -1)
        crouch = self._crouch_angle[:1].expand(num_frames)
        if (bool(self._bounce_angle[0] != 0.0)):
            crouch = crouch + self._bounce_angle[:1] * self._bounce_weight(root_pos[:, 2])
        foot_pitch = self._foot_pitch[:1].expand(num_frames)
        tar_joint_rot = self._style_pose(root_pos, root_rot, joint_rot, body_rot, swing, pose, crouch, foot_pitch=foot_pitch)
        _, tar_body_rot = self._kin_char_model.forward_kinematics(root_pos, root_rot, tar_joint_rot)
        err = self._calc_style_error(root_rot, body_rot, root_rot, tar_body_rot,
                                     self._style_joint_w(swing, pose, crouch, foot_pitch))
        return float(err.mean())

    def _calc_style_error(self, root_rot, body_rot, tar_root_rot, tar_body_rot, joint_w):
        """Error [N] of the style term: weighted mean squared angle between each body below a styled joint and
        its target, both in the heading frame of their own root (the posture seen, wherever the character faces)."""
        rot = heading_frame(root_rot, body_rot[:, 1:, :])
        tar_rot = heading_frame(tar_root_rot, tar_body_rot[:, 1:, :])
        angle = torch_util.quat_diff_angle(rot, tar_rot)
        return torch.sum(joint_w * angle * angle, dim=-1) / torch.clamp(torch.sum(joint_w, dim=-1), min=1e-6)

    def _calc_track_targets(self):
        """Targets of the DeepMimic terms (root_pos, joint_rot, dof_vel, body_pos): the reference with
        the swing scales, pose offsets and crouch applied, the foot heights raised by foot_lift, and
        the step length (thigh swing, forward reach of the feet) multiplied by the speed scale.
        Also the body rotations of the target joint rotations (for the style term, else None)."""
        root_pos = self._ref_root_pos
        joint_rot, dof_vel, body_pos = self._ref_joint_rot, self._ref_dof_vel, self._ref_body_pos
        if (self._has_pose_change()):
            joint_rot = self._calc_pose_target()
            body_pos, body_rot = self._kin_char_model.forward_kinematics(self._ref_root_pos, self._ref_root_rot, joint_rot)
            dof_vel = dof_vel * self._effective_swing(self._swing_scale)[:, self._dof_joint_ids]
            if (self._has_leg_change()):
                # The lower foot stays as high as in the reference: bent legs lower the pelvis target.
                drop = (body_pos[:, self._foot_ids, 2].min(dim=-1).values
                        - self._ref_body_pos[:, self._foot_ids, 2].min(dim=-1).values)
                if (bool(torch.any(self._foot_pitch != 0.0))):
                    # tipped feet: the lowest sole edge (toe or heel) stays as high as in the reference
                    sole = self._sole_low(body_pos, body_rot) - self._sole_low(self._ref_body_pos, self._ref_body_rot)
                    drop = torch.where(self._foot_pitch != 0.0, sole, drop)
                root_pos = root_pos.clone()
                root_pos[:, 2] -= drop
                body_pos[:, :, 2] -= drop.unsqueeze(-1)
        stride = self._has_speed()
        if (stride or "foot_lift" in self._style):
            body_pos = body_pos.clone()
        if (stride):
            # Thigh rotation and velocity targets. The foot positions are not taken from these
            # rotations: the feet keep the reference's height and only reach further forward.
            joint_rot = self._calc_pose_target(thigh_scale=self._speed_scale)
            dof_vel = dof_vel.clone()
            dof_vel[:, self._thigh_dof_ids] *= self._speed_scale.unsqueeze(-1)
            heading = torch_util.calc_heading(self._ref_root_rot)
            forward = torch.stack([torch.cos(heading), torch.sin(heading)], dim=-1).unsqueeze(1)
            reach = torch.sum((body_pos[:, self._foot_ids, 0:2] - self._ref_root_pos[:, None, 0:2]) * forward,
                              dim=-1, keepdim=True)
            body_pos[:, self._foot_ids, 0:2] += (self._speed_scale.reshape(-1, 1, 1) - 1.0) * reach * forward
        if ("foot_lift" in self._style):
            body_pos[:, self._foot_ids, 2] = self._calc_foot_target(self._ref_body_pos, self._style["foot_lift"]["scale"])
        tar_body_rot = None
        if ("style" in self._style):
            _, tar_body_rot = self._kin_char_model.forward_kinematics(self._ref_root_pos, self._ref_root_rot, joint_rot)
        return root_pos, joint_rot, dof_vel, body_pos, tar_body_rot

    def _calc_pose_target(self, thigh_scale=None):
        """Reference joint rotations [N, J, 4] with the swing scales, pose offsets and crouch applied.
        thigh_scale [N] multiplies the thighs' swing scale (the step length of the speed scale)."""
        return self._style_pose(self._ref_root_pos, self._ref_root_rot, self._ref_joint_rot, self._ref_body_rot,
                                self._swing_scale, self._pose_offset, self._crouch_now(), thigh_scale, self._foot_pitch)

    def _sole_low(self, body_pos, body_rot):
        """Height [N] of the lowest toe or heel edge of both soles."""
        pos, rot = body_pos[:, self._foot_ids, :], body_rot[:, self._foot_ids, :]
        lows = []
        for corner in self.FOOT_SOLE:
            local = torch.tensor(corner, device=pos.device, dtype=pos.dtype).expand(pos.shape)
            turned = torch_util.quat_rotate(rot.reshape(-1, 4), local.reshape(-1, 3)).reshape(pos.shape)
            lows.append(pos[..., 2] + turned[..., 2])
        return torch.stack(lows, dim=-1).amin(dim=(-1, -2))

    def _bounce_weight(self, root_z):
        """0 where the reference pelvis is at its highest in the clip, 1 where it is at its lowest."""
        span = max(self._root_h_hi - self._root_h_lo, 1e-6)
        return torch.clamp((self._root_h_hi - root_z) / span, 0.0, 1.0)

    def _crouch_now(self):
        """Crouch angle [N] at the current reference frame: crouch plus bounce times the bounce weight."""
        if (not bool(torch.any(self._bounce_angle != 0.0))):
            return self._crouch_angle
        return self._crouch_angle + self._bounce_angle * self._bounce_weight(self._ref_root_pos[:, 2])

    def _style_pose(self, ref_root_pos, ref_root_rot, ref_joint_rot, ref_body_rot, swing_scale, pose_offset,
                    crouch_angle, thigh_scale=None, foot_pitch=None):
        """_calc_pose_target for any reference frames [N] and style tensors given per frame."""
        scale = self._effective_swing(swing_scale)
        if (thigh_scale is not None):
            scale = scale.clone()
            scale[:, self._thigh_joint_ids] *= thigh_scale.unsqueeze(-1)
        swung = amplify_about_mean(ref_joint_rot, self._joint_mean_rot, scale.reshape(-1, 1))
        joint_rot = torch.where((scale != 1.0).unsqueeze(-1), swung, ref_joint_rot)
        turned = pose_offset[..., 3] != 1.0
        if (self._pose_anchor is not None):
            shape = pose_offset.shape
            pose_offset = torch_util.quat_mul(self._pose_lean.unsqueeze(0).expand(shape), torch_util.quat_mul(
                pose_offset, self._pose_anchor.unsqueeze(0).expand(shape)))
        joint_rot = torch.where(turned.unsqueeze(-1), torch_util.quat_mul(pose_offset, joint_rot), joint_rot)
        if (torch.any(crouch_angle != 0.0)):
            crouched = (crouch_angle != 0.0).unsqueeze(-1)
            zeros = torch.zeros_like(crouch_angle)
            forward = torch_util.exp_map_to_quat(torch.stack([zeros, -crouch_angle, zeros], dim=-1))
            bend = torch_util.exp_map_to_quat(torch.stack([zeros, 2.0 * crouch_angle, zeros], dim=-1))
            for thigh, shin in zip(self._thigh_joint_ids, self._shin_ids - 1):
                joint_rot[:, thigh, :] = torch_util.quat_mul(forward, joint_rot[:, thigh, :])
                joint_rot[:, shin, :] = torch_util.quat_mul(joint_rot[:, shin, :], bend)
            # Ankles, only where the legs are bent: the feet keep the reference's orientation in the world, turned
            # about the vertical as far as the thigh's pose offset turns the leg (toes out or in). Before 2026-11-11
            # the toe turn was undone, and in a batch of several styles the feet of styles without crouch were
            # also reset when any style crouched (target_features.py scores many styles at once).
            _, body_rot = self._kin_char_model.forward_kinematics(ref_root_pos, ref_root_rot, joint_rot)
            for thigh, shin, foot in zip(self._thigh_joint_ids, self._shin_ids, self._foot_ids):
                local_rot = torch.broadcast_to(self._kin_char_model._local_rotation[foot], body_rot[:, shin, :].shape)
                parent_rot = torch_util.quat_mul(body_rot[:, shin, :], local_rot)
                tar_rot = ref_body_rot[:, foot, :]
                yaw = torch_util.calc_heading(pose_offset[..., thigh, :])
                if (bool(torch.any(yaw != 0.0))):
                    zero = torch.zeros_like(yaw)
                    turn = torch_util.exp_map_to_quat(torch.stack([zero, zero, yaw], dim=-1))
                    tar_rot = torch_util.quat_mul(turn, tar_rot)
                ankle = torch_util.quat_mul(torch_util.quat_conjugate(parent_rot), tar_rot)
                joint_rot[:, foot - 1, :] = torch.where(crouched, ankle, joint_rot[:, foot - 1, :])
        if (foot_pitch is not None and bool(torch.any(foot_pitch != 0.0))):
            # feet tipped about their own lateral axis (+ toes down), after the crouch's ankles
            zeros = torch.zeros_like(foot_pitch)
            tip = torch_util.exp_map_to_quat(torch.stack([zeros, foot_pitch, zeros], dim=-1))
            tipped = (foot_pitch != 0.0).unsqueeze(-1)
            for foot in self._foot_ids:
                joint_rot[:, foot - 1, :] = torch.where(tipped, torch_util.quat_mul(joint_rot[:, foot - 1, :], tip),
                                                        joint_rot[:, foot - 1, :])
        return joint_rot

    def _has_pose_change(self):
        return bool(torch.any(self._swing_scale != 1.0) or torch.any(self._pose_offset[..., 3] != 1.0)
                    or torch.any(self._crouch_angle != 0.0) or torch.any(self._bounce_angle != 0.0)
                    or torch.any(self._foot_pitch != 0.0))

    def _has_leg_change(self):
        legs = self._leg_joint_ids
        return bool(torch.any(self._swing_scale[:, legs] != 1.0) or torch.any(self._pose_offset[:, legs, 3] != 1.0)
                    or torch.any(self._crouch_angle != 0.0) or torch.any(self._bounce_angle != 0.0)
                    or torch.any(self._foot_pitch != 0.0))

    def _has_speed(self):
        return bool(torch.any(self._speed_scale != 1.0))

    def _stretch_path(self, root_xy, start_xy, scale):
        """Root ground positions [..., 2] moved to scale times their distance from start_xy."""
        return start_xy + scale * (root_xy - start_xy)

    def _get_motion_times(self, env_ids=None):
        """Time in the clip: it runs cadence times as fast as the episode's clock."""
        if (env_ids is None):
            return self._cadence_scale * self._time_buf + self._motion_time_offsets
        return self._cadence_scale[env_ids] * self._time_buf[env_ids] + self._motion_time_offsets[env_ids]

    def _reset_ref_motion(self, env_ids):
        super()._reset_ref_motion(env_ids)
        # The stretched path starts on the reference; only the velocities differ at the start.
        self._path_start_xy[env_ids] = self._ref_root_pos[env_ids, 0:2]
        cadence = self._cadence_scale[env_ids].unsqueeze(-1)
        self._ref_root_vel[env_ids] *= cadence
        self._ref_root_ang_vel[env_ids] *= cadence
        self._ref_dof_vel[env_ids] *= cadence
        self._ref_root_vel[env_ids, 0:2] *= self._speed_scale[env_ids].unsqueeze(-1)
        if (self._has_weave()):
            self._apply_weave(env_ids)
        return

    def _update_ref_motion(self):
        super()._update_ref_motion()
        # The same motion played cadence times as fast moves cadence times as fast.
        cadence = self._cadence_scale.unsqueeze(-1)
        self._ref_root_vel *= cadence
        self._ref_root_ang_vel *= cadence
        self._ref_dof_vel *= cadence
        if (self._has_speed()):
            scale = self._speed_scale.unsqueeze(-1)
            root_xy = self._stretch_path(self._ref_root_pos[:, 0:2], self._path_start_xy, scale)
            self._ref_body_pos[:, :, 0:2] += (root_xy - self._ref_root_pos[:, 0:2]).unsqueeze(1)
            self._ref_root_pos[:, 0:2] = root_xy
            self._ref_root_vel[:, 0:2] *= scale
        if (self._has_weave()):
            self._apply_weave(None)
        return

    def _has_weave(self):
        return bool(torch.any(self._weave_amp != 0.0))

    def _weave(self, times, amp):
        """Sideways offset [..., 2] of the path and its rate per clip second, at clip times."""
        omega = 2.0 * math.pi / self.WEAVE_PERIOD_S
        heading = torch.full_like(times, self._weave_heading)
        left = torch.stack([-torch.sin(heading), torch.cos(heading)], dim=-1)
        offset = (amp * torch.sin(omega * times)).unsqueeze(-1) * left
        rate = (amp * omega * torch.cos(omega * times)).unsqueeze(-1) * left
        return offset, rate

    def _apply_weave(self, env_ids):
        """Moves the current reference frame (all environments, or env_ids) onto the weaving path."""
        ids = slice(None) if env_ids is None else env_ids
        offset, rate = self._weave(self._get_motion_times(env_ids), self._weave_amp[ids])
        self._ref_root_pos[ids, 0:2] += offset
        self._ref_body_pos[ids, :, 0:2] += offset.unsqueeze(1)
        self._ref_root_vel[ids, 0:2] += rate * self._cadence_scale[ids].unsqueeze(-1)
        return

    def _compute_obs(self, env_ids=None):
        self._obs_env_ids = env_ids  # _fetch_tar_obs_data is not told which environments it serves
        return super()._compute_obs(env_ids)

    def _fetch_tar_obs_data(self, motion_ids, motion_times):
        """The parent's future target frames, read cadence times as far ahead in the clip and on the stretched path."""
        env_ids = self._obs_env_ids
        cadence = self._cadence_scale if env_ids is None else self._cadence_scale[env_ids]
        ahead = self._engine.get_timestep() * self._tar_obs_steps
        times = motion_times.unsqueeze(-1) + cadence.unsqueeze(-1) * ahead
        ids = torch.broadcast_to(motion_ids.unsqueeze(-1), times.shape)
        root_pos, root_rot, _, _, joint_rot, _ = self._motion_lib.calc_motion_frame(ids.flatten(), times.flatten())
        root_pos = root_pos.reshape([times.shape[0], times.shape[1], root_pos.shape[-1]])
        root_rot = root_rot.reshape([times.shape[0], times.shape[1], root_rot.shape[-1]])
        joint_rot = joint_rot.reshape([times.shape[0], times.shape[1], joint_rot.shape[-2], joint_rot.shape[-1]])
        if (self._has_speed()):
            scale = self._speed_scale if env_ids is None else self._speed_scale[env_ids]
            start_xy = self._path_start_xy if env_ids is None else self._path_start_xy[env_ids]
            root_pos[..., 0:2] = self._stretch_path(root_pos[..., 0:2], start_xy.unsqueeze(1), scale.reshape(-1, 1, 1))
        if (self._has_weave()):
            amp = self._weave_amp if env_ids is None else self._weave_amp[env_ids]
            offset, _ = self._weave(times, amp.unsqueeze(-1).expand(times.shape))
            root_pos[..., 0:2] += offset
        return root_pos, root_rot, joint_rot

    def _calc_foot_target(self, ref_body_pos, scale):
        """Foot heights [N, 2] with the reference's clearance multiplied by scale."""
        ground = self._foot_ground_h.unsqueeze(0)
        return ground + scale * (ref_body_pos[:, self._foot_ids, 2] - ground)

    def _update_reward(self):
        if (not self._text_reward_ready):
            super()._update_reward()
            return

        char_id = self._get_char_id()
        root_pos = self._engine.get_root_pos(char_id)
        root_rot = self._engine.get_root_rot(char_id)
        root_vel = self._engine.get_root_vel(char_id)
        root_ang_vel = self._engine.get_root_ang_vel(char_id)
        dof_pos = self._engine.get_dof_pos(char_id)
        dof_vel = self._engine.get_dof_vel(char_id)
        body_pos = self._engine.get_body_pos(char_id)
        joint_rot = self._kin_char_model.dof_to_rot(dof_pos)

        tar_root_pos, tar_joint_rot, tar_dof_vel, tar_body_pos, tar_body_rot = self._calc_track_targets()

        r_track = deepmimic_env.compute_reward(root_pos=root_pos,
                                               root_rot=root_rot,
                                               root_vel=root_vel,
                                               root_ang_vel=root_ang_vel,
                                               joint_rot=joint_rot,
                                               dof_vel=dof_vel,
                                               key_pos=body_pos[..., self._key_body_ids, :],

                                               tar_root_pos=tar_root_pos,
                                               tar_root_rot=self._ref_root_rot,
                                               tar_root_vel=self._ref_root_vel,
                                               tar_root_ang_vel=self._ref_root_ang_vel,
                                               tar_joint_rot=tar_joint_rot,
                                               tar_dof_vel=tar_dof_vel,
                                               tar_key_pos=tar_body_pos[..., self._key_body_ids, :],

                                               joint_rot_err_w=self._joint_err_w,
                                               dof_err_w=self._dof_err_w,
                                               track_root_h=self._root_height_obs,
                                               track_root=self._track_global_root(),

                                               pose_w=self._reward_pose_w,
                                               vel_w=self._reward_vel_w,
                                               root_pose_w=self._reward_root_pose_w,
                                               root_vel_w=self._reward_root_vel_w,
                                               key_pos_w=self._reward_key_pos_w,

                                               pose_scale=self._reward_pose_scale,
                                               vel_scale=self._reward_vel_scale,
                                               root_pose_scale=self._reward_root_pose_scale,
                                               root_vel_scale=self._reward_root_vel_scale,
                                               key_pos_scale=self._reward_key_pos_scale)

        sim = (root_pos, body_pos)
        ref = (self._ref_root_pos, self._ref_body_pos)
        reward = self._track_w * r_track
        total_w = self._track_w
        for name, term in self._style.items():
            if (name == "style"):
                joint_w = self._style_joint_w(self._swing_scale, self._pose_offset, self._crouch_angle + self._bounce_angle,
                                              self._foot_pitch)
                err = self._calc_style_error(root_rot, self._engine.get_body_rot(char_id), self._ref_root_rot,
                                             tar_body_rot, joint_w)
            else:
                err = self._style_error(name, term["scale"], sim, ref)
            reward = reward + term["w"] * calc_kernel(err, self.K_FAR[name], term["k"])
            total_w += term["w"]

        self._reward_buf[:] = reward / total_w
        return

    def _style_error(self, name, scale, sim, ref):
        """Error [N] of an added term; sim and ref are (root_pos, body_pos)."""
        root_pos, body_pos = sim
        ref_root_pos, ref_body_pos = ref
        if (name == "foot_lift"):
            target = self._calc_foot_target(ref_body_pos, scale)
            return torch.sum(torch.square(target - body_pos[:, self._foot_ids, 2]), dim=-1)
        elif (name == "upright"):
            tilt = calc_tilt(body_pos[:, self._head_id, :] - root_pos)
            ref_tilt = calc_tilt(ref_body_pos[:, self._head_id, :] - ref_root_pos)
            return torch.square(tilt - scale * ref_tilt)
        assert(False), "Unsupported style term: {}".format(name)


def calc_kernel(err, k_far, k_near):
    """Mean of exp(-k * err) over the sharpness ladder k_far, sqrt(k_far * k_near), k_near."""
    k_mid = (k_far * k_near) ** 0.5
    return (torch.exp(-k_far * err) + torch.exp(-k_mid * err) + torch.exp(-k_near * err)) / 3.0


def calc_mean_quat(quat):
    """Mean rotation [J, 4] of quat [T, J, 4] (valid for rotations spread well under 180 deg)."""
    sign = torch.sign(torch.sum(quat * quat[0:1], dim=-1, keepdim=True))
    mean = torch.mean(quat * torch.where(sign == 0, torch.ones_like(sign), sign), dim=0)
    return torch_util.normalize(mean)


def amplify_about_mean(quat, mean_quat, scale):
    """quat [N, J, 4] with its rotation away from mean_quat [J, 4] multiplied by scale."""
    mean = mean_quat.unsqueeze(0).expand(quat.shape[0], quat.shape[1], 4).reshape(-1, 4)
    offset = torch_util.quat_mul(torch_util.quat_conjugate(mean), quat.reshape(-1, 4))
    scaled = torch_util.exp_map_to_quat(scale * torch_util.quat_to_exp_map(offset))
    return torch_util.quat_mul(mean, scaled).reshape(quat.shape)


def heading_frame(root_rot, rot):
    """Rotations rot [N, B, 4] turned by the inverse heading of root_rot [N, 4]."""
    heading_inv = torch_util.calc_heading_quat_inv(root_rot).unsqueeze(-2).expand(rot.shape)
    return torch_util.quat_mul(heading_inv, rot)


def calc_forward_offset(root_rot, vec):
    """Forward (heading-frame x) component of vec [N, B, 3] for root_rot [N, 4]."""
    heading_inv = torch_util.calc_heading_quat_inv(root_rot)
    heading_inv = heading_inv.unsqueeze(-2).expand(vec.shape[0], vec.shape[1], 4)
    local = torch_util.quat_rotate(heading_inv.reshape(-1, 4), vec.reshape(-1, 3))
    return local[:, 0].reshape(vec.shape[0], vec.shape[1])


def calc_tilt(up_vec):
    """Angle (rad) between up_vec [N, 3] and the world vertical."""
    horizontal = torch.linalg.vector_norm(up_vec[..., 0:2], dim=-1)
    return torch.atan2(horizontal, up_vec[..., 2])
