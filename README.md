# IP_camera_calibration
Code for capturing images containing the calibration pattern, as well as code that performs the calibration and displays the results.

## capture_images

The first step is to capture the images. Since IP cameras are used in this case, multiprocessing and multithreading is necessary.

## choose_images

With this script the final images are selected for calibration.

## calibration

This script handles the previously selected images and performs the calibration, both for each of the cameras and stereo. It also stores the data in csv files for future use.

## show_stereo_calibration / show_single_camera_calibration

with these scripts it is possible to visualise the result of the calibration.

## References

- [LearnTechWithUs/Stereo-Vision](https://github.com/LearnTechWithUs/Stereo-Vision).
