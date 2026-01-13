const CACHE_NAME = "bookstore-2048-v1";

const ASSETS = [
  "/2048",
  "/2048/index.html",
  "/book.png",
  "/logo.png",

  "/youtube.png",
  "/instagram.png",
  "/telegram.png",

  "/home.svg",
  "/game.svg",
  "/profile.svg",
  "/shiva.png",
  "/play.svg",
  "/link.svg",
  "/edupielogo.png",

  // add any other local images you use
];

// Install: cache everything
self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(ASSETS);
    })
  );
  self.skipWaiting();
});

// Activate: clean old cache
self.addEventListener("activate", event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys.map(key => {
          if (key !== CACHE_NAME) {
            return caches.delete(key);
          }
        })
      )
    )
  );
  self.clients.claim();
});

// Fetch: offline-first
self.addEventListener("fetch", event => {
  event.respondWith(
    caches.match(event.request).then(response => {
      return response || fetch(event.request);
    })
  );
});
