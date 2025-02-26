import { BrowserRouter, Route, Routes } from "react-router";
import HomePage from "./pages/HomePage";
import routes from "./utils/routes";
import CreateContactPage from "./pages/CreateContactPage";
import NotFound from "./pages/NotFound";

function AppRoutes() {
  return (
    <BrowserRouter>
      <Routes>
        <Route index element={<HomePage />} />
        <Route path={routes.createContact} element={<CreateContactPage />} />
        <Route path={routes.notFound} element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  );
}

export default AppRoutes;
