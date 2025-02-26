import AppLogo from "./components/AppLogo";
import AppRoutes from "./AppRoutes";
import styled from "styled-components";

const StyledApp = styled.div`
  font-family: "Sora";
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  height: 100vh;
`;

function App() {
  return (
    <StyledApp>
      <div style={{ width: 500 }}>
        <AppLogo />
        <AppRoutes />
      </div>
    </StyledApp>
  );
}

export default App;
