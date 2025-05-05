import axios from "axios";

export const startDetection = () =>
  axios.post(`/start-detection`);

export const stopDetection = () =>
  axios.post(`/stop-detection`);

export const toggleSound = () =>
  axios.post(`/toggle-sound`);

export const getDetections = async () => {
  const response = await axios.get(`/detections`);
  return response.data;
};
    