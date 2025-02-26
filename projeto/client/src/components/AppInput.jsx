import styled from "styled-components";
import { colors, shadows } from "../utils/styles";

const AppInput = styled.input`
    font-family: "Sora";
    font-size: 16px;
    padding: 16px;
    height: 52px;
    color: ${colors.secondary};
    border: none;
    box-sizing: border-box;
    box-shadow: ${shadows.default};
    border-radius: 4px;
    &:focus {
      outline: 2px solid ${colors.primary};
    };
    &::placeholder {
      color: ${colors.gray200}
    }
  `;

export default AppInput;
