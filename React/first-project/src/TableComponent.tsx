import React from "react";

interface User {
  name: string;
  language: string;
  id: string;
  bio: string;
  version: number;
}

const TableComponent: React.FC = () => {
  const data: User[] = [
    {
      name: "Adeel Solangi",
      language: "Sindhi",
      id: "V59OF92YF627HFY0",
      bio: "Donec lobortis eleifend condimentum. Cras dictum dolor lacinia lectus vehicula rutrum. Maecenas quis nisi nunc. Nam tristique feugiat est vitae mollis. Maecenas quis nisi nunc.",
      version: 6.1,
    },
    {
      name: "Afzal Ghaffar",
      language: "Sindhi",
      id: "ENTOCR13RSCLZ6KU",
      bio: "Aliquam sollicitudin ante ligula, eget malesuada nibh efficitur et. Pellentesque massa sem, scelerisque sit amet odio id, cursus tempor urna. Etiam congue dignissim volutpat. Vestibulum pharetra libero et velit gravida euismod.",
      version: 1.88,
    },
    {
      name: "Aamir Solangi",
      language: "Sindhi",
      id: "IAKPO3R4761JDRVG",
      bio: "Vestibulum pharetra libero et velit gravida euismod. Quisque mauris ligula, efficitur porttitor sodales ac, lacinia non ex. Fusce eu ultrices elit, vel posuere neque.",
      version: 7.27,
    },
    {
      name: "Abla Dilmurat",
      language: "Uyghur",
      id: "5ZVOEPMJUI4MB4EN",
      bio: "Donec lobortis eleifend condimentum. Morbi ac tellus erat.",
      version: 2.53,
    },
  ];

  return (
    <div>
      <h2>Users Table</h2>
      <table border={1} cellPadding="10" cellSpacing="0">
        <thead>
          <tr>
            <th>Name</th>
            <th>Language</th>
            <th>ID</th>
            <th>Bio</th>
            <th>Version</th>
          </tr>
        </thead>
        <tbody>
          {data.map((user, index) => (
            <tr key={index}>
              <td>{user.name}</td>
              <td>{user.language}</td>
              <td>{user.id}</td>
              <td>{user.bio}</td>
              <td>{user.version}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default TableComponent;
