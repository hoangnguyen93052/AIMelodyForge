import cv2
import numpy as np

class ARMarker:
    def __init__(self, marker_id, size=100):
        self.marker_id = marker_id
        self.size = size
        self.marker_image = None
        self.create_marker()

    def create_marker(self):
        self.marker_image = np.zeros((self.size, self.size), dtype=np.uint8)
        cv2.circle(self.marker_image, (self.size//2, self.size//2), self.size//4, 255, -1)
        cv2.putText(self.marker_image, str(self.marker_id), (self.size//4, self.size//2), cv2.FONT_HERSHEY_SIMPLEX, 1, 0, 2)
        self.marker_image = cv2.cvtColor(self.marker_image, cv2.COLOR_GRAY2BGR)

class ARApp:
    def __init__(self):
        self.markers = []
        self.cap = cv2.VideoCapture(0)
        self.load_markers()

    def load_markers(self):
        for i in range(3):
            marker = ARMarker(marker_id=i + 1)
            self.markers.append(marker)

    def detect_markers(self, frame):
        # Convert frame to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Marker detection logic here (simplified for demonstration)
        detected_markers = []
        for marker in self.markers:
            result = cv2.matchTemplate(gray_frame, marker.marker_image[:, :, 0], cv2.TM_CCOEFF_NORMED)
            if np.max(result) > 0.8:
                detected_markers.append(marker.marker_id)
        return detected_markers

    def overlay_marker(self, frame, marker_id):
        text = f'You detected marker {marker_id}'
        position = (50, 50)
        cv2.putText(frame, text, position, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    def run(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            detected_markers = self.detect_markers(frame)
            for marker_id in detected_markers:
                self.overlay_marker(frame, marker_id)

            cv2.imshow('AR App', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    ar_app = ARApp()
    ar_app.run()