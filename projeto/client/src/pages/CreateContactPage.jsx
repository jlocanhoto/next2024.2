import styled from "styled-components";
import backIcon from "../assets/back-icon.svg";
import AppButton from "../components/AppButton";
import AppInput from "../components/AppInput";
import { colors } from "../utils/styles";
import { useNavigate } from "react-router";
import { useState } from "react";
import routes from "../utils/routes";
import { isRouteErrorResponse } from "react-router";

const StyledForm = styled.form`
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-top: 16px;
`;

function CreateContactPage() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const navigate = useNavigate();

  const goBack = () => {
    navigate(-1);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    const baseApiUrl = import.meta.env.VITE_API_URL;

    fetch(`${baseApiUrl}/contacts`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ name, email, phone }),
    }).then(navigate(routes.home));
  };

  return (
    <>
      <AppButton icon={backIcon} onClick={goBack}>
        Voltar
      </AppButton>

      <h1 style={{ color: colors.secondary, margin: "16px 0 0 0" }}>
        Novo contato
      </h1>

      <StyledForm onSubmit={(event) => handleSubmit(event)}>
        <AppInput
          type="text"
          placeholder="Nome"
          value={name}
          onChange={({ target }) => setName(target.value)}
          required
        />
        <AppInput
          type="email"
          placeholder="E-mail"
          value={email}
          onChange={({ target }) => setEmail(target.value)}
          required
        />
        <AppInput
          type="tel"
          placeholder="Telefone"
          value={phone}
          onChange={({ target }) => setPhone(target.value)}
          required
        />
        <AppButton variant="contained" disabled={!name || !email || !phone}>
          Cadastrar
        </AppButton>
      </StyledForm>
    </>
  );
}

export default CreateContactPage;
