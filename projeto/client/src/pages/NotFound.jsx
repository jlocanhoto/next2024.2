import styled from "styled-components";
import { useNavigate } from "react-router";
import { colors } from "../utils/styles";

const Container = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
`

const NotFoundText = styled.p`
  font-family: "Sora";
`

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

function NotFound() {
  const navigate = useNavigate()

  const goHome = () => {
    navigate('/')
  }
  return (
    <Container>
      <NotFoundText>Página Não Encontrada</NotFoundText>
      <BaseButton onClick={() => goHome()} type="button">Voltar</BaseButton>
    </Container>
  )
}

export default NotFound;