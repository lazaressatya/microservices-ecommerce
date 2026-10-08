const express = require("express");
const mongoose = require("mongoose");

const app = express();

app.use(express.json());

const PORT = process.env.PORT || 3001;
const MONGODB_URI =
  process.env.MONGODB_URI || "mongodb://user-mongodb:27017/usersdb";

mongoose
  .connect(MONGODB_URI)
  .then(() => console.log("Connected to MongoDB"))
  .catch((err) => console.error("MongoDB connection error:", err));

const userSchema = new mongoose.Schema(
  {
    name: {
      type: String,
      required: true
    },
    email: {
      type: String,
      required: true,
      unique: true
    }
  },
  {
    timestamps: true
  }
);

const User = mongoose.model("User", userSchema);

app.get("/", (req, res) => {
  res.json({
    service: "User Service",
    status: "running"
  });
});

app.get("/health", (req, res) => {
  res.json({
    status: "UP",
    service: "user-service"
  });
});

app.get("/users", async (req, res) => {
  try {
    const users = await User.find();
    res.json(users);
  } catch (error) {
    res.status(500).json({
      error: error.message
    });
  }
});

app.post("/users", async (req, res) => {
  try {
    const user = await User.create(req.body);
    res.status(201).json(user);
  } catch (error) {
    res.status(500).json({
      error: error.message
    });
  }
});

app.listen(PORT, "0.0.0.0", () => {
  console.log(`User Service running on port ${PORT}`);
});