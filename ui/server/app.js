"use strict";

const fastify = require("fastify");

function createApp({ logger }) {
  const app = fastify({ logger });

  // Define routes
  app.get("/", async (request, reply) => {
    return { hello: "world" };
  });

  // Define routes
  app.get("/api", async (request, reply) => {
    return { hello: "world" };
  });

  return app;
}

module.exports = createApp;
