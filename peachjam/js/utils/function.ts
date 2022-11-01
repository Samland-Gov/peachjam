// Reusable utility functions

export function scrollToElement (elem: HTMLElement, offset = 0) {
  const rect = elem.getBoundingClientRect();
  const targetPosition = Math.floor(rect.top + self.pageYOffset - offset);
  window.scrollTo({
    top: targetPosition,
    behavior: 'smooth'
  });
  return new Promise((resolve, reject) => {
    window.setTimeout(() => {
      // Reject promise after 5s
      reject(new Error('Timed out. Took too long to intersect target element'));
    }, 5000);
    const observer = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          observer.unobserve(entry.target);
          window.setTimeout(() => { resolve(elem); }, 1000);
        }
      });
    });
    observer.observe(elem);
  });
}

export const getUserLocale = () => navigator.languages && navigator.languages.length
  ? navigator.languages[0]
  : navigator.language;
