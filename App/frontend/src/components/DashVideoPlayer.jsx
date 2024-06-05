import React, { useEffect, useRef } from 'react';
import dashjs from 'dashjs';

export default function DashVideoPlayer({ url, startTime, endTime }) {
  const videoRef = useRef(null);

  useEffect(() => {
    const videoElement = videoRef.current;
    if (videoElement) {
      const player = dashjs.MediaPlayer().create();
      player.initialize(videoElement, url, false);

      // Set the initial playback time
      player.on(dashjs.MediaPlayer.events.STREAM_INITIALIZED, () => {
        if (startTime) {
          player.seek(startTime);
        }
      });

      // Add an event listener to handle the end of the fragment
      if (endTime) {
        const onTimeUpdate = () => {
          if (videoElement.currentTime >= endTime) {
            videoElement.pause();
            player.seek(startTime);
          }
        };
        videoElement.addEventListener('timeupdate', onTimeUpdate);
      }

      return () => {
        player.destroy();
      };
    }
  }, []);

  return (
    <div>
      <video
        ref={videoRef}
        controls
        style={{ width: '100%', height: '100%' }}
      ></video>
    </div>
  );
};
