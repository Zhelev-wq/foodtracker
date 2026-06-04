import { components } from "../types/api";
import { useState } from "react";
import { api } from "../api/client.ts";

export default function Register() {
  const handleSubmit = async (e) => {
    if (password !== confirmPassword) {
      throw Error("passwords don't match");
    }
    const response = await api.post("/api/users", {
      name: name,
      email: username,
      password: password,
    });
    if (response.status == 201) {
      window.location.href = "/login";
    }

    if (response.status == 422) {
      throw Error(`validation error ${response.statusText}`);
    }
  };

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [name, setName] = useState("");

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Email: </label>
          <input
            name="username"
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>
        <div>
          <label>Name: </label>
          <input
            name="name"
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
        </div>
        <div>
          <label>Password: </label>
          <input
            name="password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <div>
          <label>Confirm Password: </label>
          <input
            name="confirmPassword"
            type="password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
          />
        </div>
        <button type="submit">Create Account</button>
      </form>
    </div>
  );
}
