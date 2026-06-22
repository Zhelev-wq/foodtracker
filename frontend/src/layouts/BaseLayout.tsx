import { ReactNode } from "react";
import { ROUTES } from "../routes";
import { useNavigate, Link } from "react-router";

type BaseLayoutProps = {
  children: ReactNode;
};

function handleLogOut() {
  const navigate = useNavigate();
  const token = localStorage.getItem("token");
  if (!token) {
    return null;
  }
  localStorage.removeItem("token");
  navigate(ROUTES.LOGIN)
}

export default function BaseLayout({ children }: BaseLayoutProps) {
  return (
    <div>
      <header>
        <div>
          <Link to={ROUTES.TRACKER}>
            <button>Home</button>
          </Link>
          <Link to={ROUTES.CUSTOM_FOODS}>
            <button>Custom Foods</button>
          </Link>
          <Link to={ROUTES.STATISTICS}>
            <button>Statistics</button>
          </Link>
          <button onClick={handleLogOut}>Log Out</button>
        </div>
      </header>
      {children}
    </div>
  );
}
