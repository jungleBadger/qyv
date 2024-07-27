const dotenv = require("dotenv");
const path = require("path");
const createApp = require("./server/app");
const fastifyStatic = require("@fastify/static");
const pino = require("pino");

// Load environment variables
dotenv.config();

const host = process.env.APP_HOST || "0.0.0.0";
const port = process.env.APP_PORT || 3000;
const debug = process.env.DEBUG === "true";

const logger = pino({
  level: debug ? "debug" : "info",
  transport: {
    target: "pino-pretty",
    options: {
      colorize: true,
      translateTime: true,
      ignore: "pid,hostname"
    }
  }
});
const app = createApp({ logger });

app.register(fastifyStatic, {
  root: path.join(__dirname, "../ui/client/user_module/dist"),
  prefix: "/", // optional: default '/'
  decorateReply: true // Do not decorate the reply interface
});

// Register the @fastify/static plugin for serving static files from admin_module
app.register(fastifyStatic, {
  root: path.join(__dirname, "../ui/client/admin_module/dist"),
  prefix: "/admin_static/", // optional: default '/'
  decorateReply: false // Do not decorate the reply interface
});

// Serve the index.html file
app.get("/app", (request, reply) => {
  reply.sendFile(
    "index.html",
    path.join(__dirname, "../ui/client/user_module/dist")
  ); // serving the index.html from user_module/dist
});

// Serve the index.html file
app.get("/admin", (request, reply) => {
  reply.sendFile(
    "index.html",
    path.join(__dirname, "../ui/client/admin_module/dist")
  ); // serving the index.html from admin_module/dist
});

// Start the server with the new method
app.listen({ port, host }, (err, address) => {
  if (err) {
    app.log.error(err);
    process.exit(1);
  }
});
