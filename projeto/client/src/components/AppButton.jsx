import styled from "styled-components";
import { colors } from "../utils/styles";
import { useMemo } from "react";

const BaseButton = styled.button`
  font-family: "Sora";
  display: flex;
  justify-content: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
  color: ${colors.primary};
  background-color: white;
  border: none;
  padding: 0px;
  border-radius: 24px;
  cursor: pointer;
  &:disabled {
    cursor: auto;
  }
`;

const OutlinedButton = styled(BaseButton)`
  border: 2px solid ${colors.primary};
  padding: 10px 16px;
`;

const ContainedButton = styled(BaseButton)`
  padding: 10px 16px;
  background-color: ${colors.primary};
  color: white;
  &:disabled {
    background-color: ${colors.gray200};
  }
`;

function AppButton({ variant, icon, children, ...buttonProps }) {
  const Button = useMemo(() => {
    switch (variant) {
      case "outlined":
        return OutlinedButton;
      case "contained":
        return ContainedButton;
      default:
        return BaseButton;
    }
  }, [variant]);

  return (
    <Button {...buttonProps}>
      {icon && <img src={icon} />}
      {children && <span>{children}</span>}
    </Button>
  );
}

export default AppButton;
