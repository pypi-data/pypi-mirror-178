import $ from 'jquery';

const debounce = (callback, wait) => {
  let timeoutId = null;

  return (...args) => {
    window.clearTimeout(timeoutId);
    timeoutId = window.setTimeout(() => {
      callback(...args);
    }, wait);
  };
};

/**
 * Format the time from seconds to HH:MM:SS.
 * @param {Number} seconds
 * @return {String}
 */
const formatDuration = (seconds) => {
  return new Date(1000 * seconds).toISOString().substr(11, 8);
};

$(function () {
  const fileInput = document.querySelector('input#id_sound_file');
  const currentFileUrl = document.querySelector(
    '[data-contentpath="sound_file"] a'
  );
  const urlInput = document.querySelector('input#id_sound_url');
  const durationInput = document.querySelector('input#id_duration');
  const isValidInput = document.querySelector('input#id_is_sound_valid');

  // Retreive the audio source (external or internal url) from the form fields
  const getSource = () => {
    if (currentFileUrl) {
      return currentFileUrl.href;
    }

    if (urlInput) {
      return urlInput.value;
    }
  };

  // Create a new Audio object with the current sound_url value or the sound
  // file to validate it and set the duration value with the audio duration
  const retrieve = debounce((src) => {
    isValidInput.value = '0';

    if (!src) {
      durationInput.value = '';
      return;
    }

    const audio = new Audio();
    audio.preload = 'metadata';

    audio.addEventListener('error', () => {
      durationInput.value = '';
    });
    audio.addEventListener('loadedmetadata', () => {
      isValidInput.value = '1';
      durationInput.value =
        audio.duration === Infinity ? '' : formatDuration(audio.duration);
    });

    audio.src = src;
  }, 500);

  urlInput.addEventListener('input', () => {
    retrieve(urlInput.value);
  });
  if (fileInput) {
    fileInput.addEventListener('input', () => {
      const tmpUrl = URL.createObjectURL(fileInput.files[0]);
      retrieve(tmpUrl);
    });
  }

  retrieve(getSource());
});
