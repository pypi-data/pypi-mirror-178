#ifndef CPP_INCLUDE_EYEREC_PUPILDETECTIONMETHOD_H
#define CPP_INCLUDE_EYEREC_PUPILDETECTIONMETHOD_H

#include <bitset>
#include <deque>
#include <string>

#include <opencv2/core.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>

#include "eyerec/Pupil.hpp"

struct DetectionParameters {
    // Only search within this region of interest (but the whole frame is used
    // to derive parameters)
    cv::Rect roi = { 0, 0, 0, 0 };
    float userMinPupilDiameterPx = -1;
    float userMaxPupilDiameterPx = -1;
    // If true and the detection method doesn't implement a confidence metric,
    // use internal confidence metric
    bool provideConfidence = true;
};

class PupilDetectionMethod {
public:
    virtual ~PupilDetectionMethod() = default;

    Pupil detect(const cv::Mat& frame, DetectionParameters params);

    virtual bool hasConfidence() = 0;
    virtual bool hasCoarseLocation() = 0;
    virtual std::string description() = 0;

    // Generic coarse pupil detection
    static cv::Rect coarsePupilDetection(const cv::Mat& frame,
        const float& minCoverage = 0.5f, const int& workingWidth = 60,
        const int& workingHeight = 40);

    // Generic confidence metrics
    static float outlineContrastConfidence(
        const cv::Mat& frame, const Pupil& pupil, const int& bias = 5);
    static float edgeRatioConfidence(const cv::Mat& edgeImage,
        const Pupil& pupil, std::vector<cv::Point>& edgePoints,
        const int& band = 5);
    static float angularSpreadConfidence(
        const std::vector<cv::Point>& points, const cv::Point2f& center);
    static float aspectRatioConfidence(const Pupil& pupil);
    static float ellipseDistanceConfidence(const Pupil& pupil,
        const std::vector<cv::Point>& edgePoints,
        std::vector<cv::Point>& validPoints, const int& dist = 3);

protected:
    virtual Pupil implDetect(const cv::Mat& frame, DetectionParameters params)
        = 0;
};

#endif // CPP_INCLUDE_EYEREC_PUPILDETECTIONMETHOD_H
