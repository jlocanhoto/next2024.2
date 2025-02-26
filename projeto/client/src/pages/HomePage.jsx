import { useNavigate } from "react-router";
import AppButton from "../components/AppButton";
import ContactCard from "../components/ContactCard";
import EmptyList from "../components/EmptyList";
import { colors } from "../utils/styles";
import routes from "../utils/routes";
import styled from "styled-components";
import { useEffect, useState } from "react";

const Header = styled.header`
  border-bottom: 2px solid ${colors.gray100};
  padding-bottom: 16px;
`;

function HomePage() {
  const [contactList, setContactList] = useState([]);
  const navigate = useNavigate();
  const baseApiUrl = import.meta.env.VITE_API_URL;

  const newContact = () => {
    navigate(routes.createContact);
  };

  const fetchContacts = () => {
    fetch(`${baseApiUrl}/contacts`)
      .then((response) => response.json())
      .then((data) => setContactList(data));
  };

  const handleDelete = (contactId) => {
    console.log(contactId);
    fetch(`${baseApiUrl}/contacts/${contactId}`, {
      method: "DELETE",
    }).then(fetchContacts);
  };

  useEffect(() => {
    fetchContacts();
  }, []);

  return (
    <>
      <Header>
        <AppButton variant="outlined" onClick={newContact}>
          Novo contato
        </AppButton>
      </Header>
      <main>
        {contactList.length ? (
          contactList.map((contact) => (
            <ContactCard
              key={contact.id}
              contact={contact}
              onDelete={handleDelete}
            />
          ))
        ) : (
          <EmptyList />
        )}
      </main>
    </>
  );
}

export default HomePage;
