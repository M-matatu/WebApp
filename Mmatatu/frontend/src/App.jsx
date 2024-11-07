import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import ProtectedRoute from "./@protect/ProtectedRoute";
import Login from "./auth/login/login";
import Register from "./auth/register/register";
import Dashboard from "./dashboard/page";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        

        {/* Protect these routes */}
        { <Route
          path="/dashboard"
          element={<ProtectedRoute element={<Dashboard />} />}
        /> }
      </Routes>
    </Router>
  );
}

export default App;
