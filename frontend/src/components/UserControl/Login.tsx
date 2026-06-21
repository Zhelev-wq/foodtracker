import { api } from "../../api/client.ts";
import { useState } from "react";

type LoginProps = {};

export default function Login({}: LoginProps) {
  const loggedIn = () => {
    const token = localStorage.getItem("token");
    if (token) {
      return true;
    }
    return false;
  };

  const handleSubmit = async (e: React.ChangeEvent<HTMLFormElement>) => {
    e.preventDefault();

    const formData = new URLSearchParams();
    formData.append("username", username);
    formData.append("password", password);

    const res = await api.post("/api/users/token", formData);
    localStorage.setItem("token", res.data.access_token);
    window.location.href = "/";
  };

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  if (!loggedIn()) {
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
            <label>Password: </label>
            <input
              name="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
          <button type="submit">Log In</button>
        </form>
        <a href="/register">Register here</a>
      </div>
    );
  }
  return (
    <div>
      <p>User already logged in</p>
    </div>
  );
}
