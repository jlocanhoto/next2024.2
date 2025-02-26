import { colors, shadows } from "../utils/styles";
import deleteIcon from "../assets/delete-icon.svg";
import AppButton from "./AppButton";
import styled from "styled-components";

const Card = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 16px;
  padding: 16px;
  box-shadow: ${shadows.default};
  border-radius: 4px;
`;

const CardContent = styled.div`
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-size: 14px;
  color: ${colors.gray200};
`;

const CardTitle = styled.div`
  font-size: 16px;
  font-weight: 600;
  color: ${colors.secondary};
`;

function ContactCard({ contact, onDelete }) {
  return (
    <Card>
      <CardContent>
        <CardTitle>{contact.name}</CardTitle>
        <div>{contact.email}</div>
        <div>{contact.phone}</div>
      </CardContent>
      <div>
        <AppButton
          icon={deleteIcon}
          title="Excluir contato"
          onClick={() => onDelete(contact.id)}
        />
      </div>
    </Card>
  );
}

export default ContactCard;
