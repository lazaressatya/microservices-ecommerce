const express = require("express");
const { createClient } = require("redis");

const app = express();

app.use(express.json());

const PORT = 3007;

const redisClient = createClient({
  url: process.env.REDIS_URL || "redis://notification-redis:6379"
});

redisClient.on("error", (error) => {
  console.error("Redis Error:", error);
});

async function start() {

  await redisClient.connect();

  console.log("Connected to Redis");

  app.get("/", (req, res) => {

    res.json({
      service: "Notification Service",
      status: "running"
    });

  });

  app.get("/health", (req, res) => {

    res.json({
      service: "notification-service",
      status: "UP"
    });

  });

  app.post("/notifications", async (req, res) => {

    const notification = req.body;

    await redisClient.lPush(
      "notifications",
      JSON.stringify(notification)
    );

    res.status(201).json({
      message: "Notification stored",
      notification
    });

  });

  app.get("/notifications", async (req, res) => {

    const notifications =
      await redisClient.lRange(
        "notifications",
        0,
        -1
      );

    res.json(
      notifications.map(
        item => JSON.parse(item)
      )
    );

  });

  app.listen(
    PORT,
    "0.0.0.0",
    () => {
      console.log(
        `Notification Service running on ${PORT}`
      );
    }
  );
}

start();