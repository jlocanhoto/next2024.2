import { colors } from "../utils/styles";
import image from "../assets/empty-box.svg";
import styled from "styled-components";

const Container = styled.div`
  display: flex;
  align-items: center;
  flex-direction: column;
  margin-top: 32px;
  text-align: center;
`;

const Message = styled.div`
  color: ${colors.gray200};
  font-size: 16px;
  width: 400px;
`;

function EmptyList() {
  return (
    <Container>
      <img src={image} />
      <Message>
        Você ainda não tem nenhum contato cadastrado! Clique no botão
        <strong style={{ color: colors.primary }}>“Novo contato”</strong> acima
        para cadastrar o seu primeiro!
      </Message>
    </Container>
  );
}

export default EmptyList;
