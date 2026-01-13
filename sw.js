const CACHE_NAME = "bookstore-2048-v1";
const FILES = [
  "./",
  "./index.html",
  "./logo.png",
  "./book.png",
  "./icons/youtube.png",
  "./icons/instagram.png",
  "./icons/telegram.png"
];

self.addEventListener("install", e => {
  e.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(FILES))
  );
});

self.addEventListener("fetch", e => {
  e.respondWith(
    caches.match(e.request).then(res => res || fetch(e.request))
  );
});
