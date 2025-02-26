import {colors} from "../utils/styles";

function AppLogo() {
  const h1Style = {
    color: colors.secondary,
    marginBottom: 32,
    textAlign: 'center'
  };
  return (
    <h1 style={h1Style}>
      Keep<span style={{ color: colors.primary }}>Connect</span>
    </h1>
  );
}

export default AppLogo;
