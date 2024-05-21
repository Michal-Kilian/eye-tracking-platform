import cv2
import numpy as np
from pupil_labs.realtime_api.simple import discover_one_device
from backend.Helpers import MathHelpers
from pupil_detectors import Detector2D
from pye3d.detector_3d import Detector3D, CameraModel, DetectorMode
import time


class PoseSolver:

    def __init__(self, markerLength, cameraMatrix, distortionCoeffs):
        detectorDictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
        detectorParameters = cv2.aruco.DetectorParameters()
        self._arucoDetector = cv2.aruco.ArucoDetector(detectorDictionary, detectorParameters)
        self._markerLength = markerLength
        self._cm = cameraMatrix
        self._dcs = distortionCoeffs
        return

    def _solveRotation(self, tvecDict):
        avg13 = (tvecDict[1] + tvecDict[3]) * 0.5
        avg02 = (tvecDict[0] + tvecDict[2]) * 0.5
        xVec = avg13 - avg02

        avg01 = (tvecDict[0] + tvecDict[1]) * 0.5
        avg23 = (tvecDict[2] + tvecDict[3]) * 0.5
        yVec = avg01 - avg23

        nxVec = MathHelpers.normalize(xVec).ravel()
        nyVec = MathHelpers.normalize(yVec).ravel()
        nzVec = MathHelpers.normalize(MathHelpers.cross_product(nxVec, nyVec)).ravel()

        rotMat = np.array([
            [nxVec[0], nyVec[0], nzVec[0]],
            [nxVec[1], nyVec[1], nzVec[1]],
            [nxVec[2], nyVec[2], nzVec[2]]]
        )
        return rotMat

    def getPose(self, image, debugImage=None):
        corners, ids, _ = self._arucoDetector.detectMarkers(image)
        if len(corners) > 3:
            totalTvec = np.zeros(3)
            tvecDict = {}

            for i in range(len(ids)):
                mid = ids[i][0]
                if mid <= 3:
                    rvec, tvec, _ = cv2.aruco.estimatePoseSingleMarkers(
                        corners[i],
                        self._markerLength,
                        self._cm,
                        self._dcs
                    )
                    totalTvec += tvec.ravel()
                    tvecDict[mid] = tvec.ravel()

                    if debugImage is not None:
                        cv2.aruco.drawDetectedMarkers(debugImage, corners, ids)
                        cv2.drawFrameAxes(
                            debugImage,
                            self._cm,
                            self._dcs,
                            rvec,
                            tvec,
                            100
                        )

            if len(tvecDict) != 4:
                return None

            meanTvec = totalTvec / len(totalTvec)
            rotMat = self._solveRotation(tvecDict)

            if debugImage is not None:
                rvec, _ = cv2.Rodrigues(rotMat)
                cv2.drawFrameAxes(
                    debugImage,
                    self._cm,
                    self._dcs,
                    rvec,
                    meanTvec,
                    100
                )

            return rotMat, meanTvec

        return None


class EyeSolver:

    def __init__(self, focalLength, properties2D={}, properties3D={}):
        self._focalLength = focalLength
        self._detector2D = Detector2D(properties2D)
        self._detector3D = None
        self._properties3D = properties3D
        self._lastResult3D = None
        return

    def update(self, image, debugImage=None, confidence=0.5):
        if self._detector3D is None:
            camera = CameraModel(focal_length=self._focalLength, resolution=image.shape[::-1])
            self._detector3D = Detector3D(camera=camera, long_term_mode=DetectorMode.blocking)
            self._detector3D.update_properties(self._properties3D)

        result2D = self._detector2D.detect(image)
        result2D["timestamp"] = time.time()

        if result2D["confidence"] > confidence:
            self._lastResult3D = self._detector3D.update_and_detect(result2D, image)

        if debugImage is not None and self._lastResult3D is not None:
            try:
                ellipse = self._lastResult3D["ellipse"]
                cv2.ellipse(
                    debugImage,
                    tuple(int(v) for v in ellipse["center"]),
                    tuple(int(v / 2) for v in ellipse["axes"]),
                    ellipse["angle"],
                    0,
                    360,
                    (0, 255, 0),
                )
                ellipse = self._lastResult3D['projected_sphere']
                cv2.ellipse(
                    debugImage,
                    [int(e) for e in ellipse['center']],
                    [int(e / 2) for e in ellipse['axes']],
                    ellipse['angle'],
                    0,
                    360,
                    (0, 255, 0),
                    2
                )
            except Exception as e:
                print(e)
        return self._lastResult3D

    def reset(self):
        self._detector3D.reset()
        return


class GazeSolver:

    def __init__(self, eyeCamPos, eyeCamRot, displayWidth, displayHeight):
        self._eyeCamPos = eyeCamPos
        self._eyeCamRot = eyeCamRot
        self._forward = np.array([0, 0, 1])
        self._displayWidth = displayWidth
        self._displayHeight = displayHeight
        return

    def _getIntersectionWcs(self, eyeCenter, eyeNormal, displayPos, displayRot):
        # """
        eyePositionWcs = MathHelpers.transform(
            eyeCenter,
            self._eyeCamPos, self._eyeCamRot
        )
        print("eyepos:", eyePositionWcs)
        gazeDirWcs = MathHelpers.normalize(
            MathHelpers.rotate(
                eyeNormal,
                self._eyeCamRot
            )
        )
        print("eyedir:", gazeDirWcs)
        # """
        """
        eyePositionWcs = eyeCenter
        gazeDirWcs = eyeNormal
        """
        displayNormalWcs = MathHelpers.normalize(MathHelpers.rotate(self._forward, displayRot))
        print("displayPos:", displayPos)
        print("dispNormal:", displayNormalWcs)
        intersectionTime = MathHelpers.intersect_plane(
            displayNormalWcs, displayPos,
            eyePositionWcs, gazeDirWcs
        )
        if intersectionTime < 0:
            return None
        planeIntersectionWcs = MathHelpers.get_point([eyePositionWcs, gazeDirWcs], intersectionTime)
        return planeIntersectionWcs

    def _getUV(self, intersectionWcs, displayPos, displayRot):
        print("wcs:", intersectionWcs)
        intersectionLocal = MathHelpers.inverse_transform(
            intersectionWcs,
            displayPos,
            displayRot
        )
        print("local:", intersectionLocal)
        uvCoords = MathHelpers.convert_to_uv(
            intersectionLocal,
            self._displayWidth,
            self._displayHeight,
            include_outliers=True
        )
        print("uv:", uvCoords)
        return uvCoords

    def getGazeUV(self, eyeCenter, eyeNormal, displayPos, displayRot):
        ret = self._getIntersectionWcs(eyeCenter, eyeNormal, displayPos, displayRot)
        if ret is not None:
            ret = self._getUV(ret, displayPos, displayRot)
        return ret


def main():
    # Look for devices. Returns as soon as it has found the first device.
    print("Looking for the next best device...")
    device = discover_one_device(max_search_duration_seconds=10)
    if device is None:
        print("No device found.")
        raise SystemExit(-1)

    print(f"Connecting to {device}...")
    displayWH = (301, 188)
    calibration = device.get_calibration()
    poseSolver = PoseSolver(37, calibration["scene_camera_matrix"][0], calibration["scene_distortion_coefficients"][0])

    lcm = calibration["left_camera_matrix"][0]
    rcm = calibration["right_camera_matrix"][0]
    lcRot = calibration["left_extrinsics_affine_matrix"][0, 0:3, 0:3]
    lcPos = calibration["left_extrinsics_affine_matrix"][0, 0:3, 3]
    rcRot = calibration["right_extrinsics_affine_matrix"][0, 0:3, 0:3]
    rcPos = calibration["right_extrinsics_affine_matrix"][0, 0:3, 3]
    leftEyeSolver = EyeSolver((lcm[0, 0] + lcm[1, 1]) * 0.5)
    rightEyeSolver = EyeSolver((rcm[0, 0] + rcm[1, 1]) * 0.5)
    leftGazeSolver = GazeSolver(lcPos, lcRot, *displayWH)
    rightGazeSolver = GazeSolver(rcPos, rcRot, *displayWH)

    cv2.namedWindow("Gaze Debug", cv2.WINDOW_NORMAL)
    cv2.setWindowProperty("Gaze Debug", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    try:
        while True:
            matched = device.receive_matched_scene_and_eyes_video_frames_and_gaze()
            if not matched:
                print(
                    "Not able to find a match! Note: Pupil Invisible does not support "
                    "streaming eyes video"
                )
                continue

            colorLeft, colorRight = np.hsplit(matched.eyes.bgr_pixels, 2)
            grayLeft, grayRight = np.hsplit(cv2.cvtColor(matched.eyes.bgr_pixels, cv2.COLOR_BGR2GRAY), 2)
            leftResult = leftEyeSolver.update(np.ascontiguousarray(grayLeft), colorLeft)
            rightResult = rightEyeSolver.update(np.ascontiguousarray(grayRight), colorRight)
            cv2.imshow("Left eye", colorLeft)
            cv2.imshow("Right eye", colorRight)

            colorWorld = matched.scene.bgr_pixels
            grayWorld = cv2.cvtColor(colorWorld, cv2.COLOR_BGR2GRAY)
            colorWorld = (colorWorld * 0.1).astype(np.uint8)
            pose = poseSolver.getPose(grayWorld, colorWorld)

            if pose is not None and leftResult is not None and rightResult is not None:
                print("HERE")
                """
                leftCenter = np.array([
                    matched.gaze.eyeball_center_left_x,
                    matched.gaze.eyeball_center_left_y,
                    matched.gaze.eyeball_center_left_z
                ])
                leftNormal = np.array([
                    matched.gaze.optical_axis_left_x,
                    matched.gaze.optical_axis_left_y,
                    matched.gaze.optical_axis_left_z
                ])
                rightCenter = np.array([
                    matched.gaze.eyeball_center_right_x,
                    matched.gaze.eyeball_center_right_y,
                    matched.gaze.eyeball_center_right_z
                ])
                rightNormal = np.array([
                    matched.gaze.optical_axis_right_x,
                    matched.gaze.optical_axis_right_y,
                    matched.gaze.optical_axis_right_z
                ])
                leftUV = leftGazeSolver.getGazeUV(
                    leftCenter,
                    leftNormal,
                    pose[1],
                    pose[0]
                )
                rightUV = rightGazeSolver.getGazeUV(
                    rightCenter,
                    rightNormal,
                    pose[1],
                    pose[0]
                )

                """

                leftUV = leftGazeSolver.getGazeUV(
                    np.array(leftResult["sphere"]["center"]),
                    np.array(leftResult["circle_3d"]["normal"]),
                    pose[1],
                    pose[0]
                )
                rightUV = rightGazeSolver.getGazeUV(
                    np.array(rightResult["sphere"]["center"]),
                    np.array(rightResult["circle_3d"]["normal"]),
                    pose[1],
                    pose[0]
                )

                if leftUV is not None and rightUV is not None:
                    combinedUV = (leftUV + rightUV) * 0.5

                    pixelCoords = (
                        int(combinedUV[0] * colorWorld.shape[1]),
                        int(combinedUV[1] * colorWorld.shape[0])
                    )
                    cv2.circle(colorWorld, pixelCoords, 10, (0, 0, 255), 2)

            cv2.imshow("Gaze Debug", colorWorld)

            waitedKey = cv2.waitKey(1) & 0xFF
            if waitedKey == 27:
                break
            elif waitedKey == ord('r'):
                leftEyeSolver.reset()
                rightEyeSolver.reset()
    except KeyboardInterrupt:
        pass
    finally:
        print("Stopping...")
        device.close()  # explicitly stop auto-update
        cv2.destroyWindow("Gaze Debug")


if __name__ == "__main__":
    main()