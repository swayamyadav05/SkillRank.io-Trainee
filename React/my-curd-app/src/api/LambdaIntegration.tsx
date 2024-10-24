interface User {
  _id: string;
  name: string;
  language: string;
  id: string;
  bio: string;
  version: number;
}

type UserUpdateData = Omit<User, "_id">;

const generateCustomID = (): string => {
  return Math.random().toString(36).substring(2, 15).toUpperCase();
};

// Fetch all users from Lambda
export const fetchUsers = async (): Promise<User[] | undefined> => {
  try {
    const response = await fetch(
      "https://njzudhkqwg.execute-api.us-east-1.amazonaws.com/default/api/data"
    );

    if (!response.ok) {
      console.error("Error fetching users:", await response.text());
      return undefined;
    }

    const users: User[] = await response.json();
    return users;
  } catch (error) {
    console.error("Error:", error);
    return undefined;
  }
};

// Create a new user in Lambda
export const createUser = async (formData: User): Promise<void> => {
  try {
    const newUserData = {
      name: formData.name,
      language: formData.language,
      id: generateCustomID(),
      bio: formData.bio,
      version: formData.version,
    };
    const response = await fetch(
      "https://njzudhkqwg.execute-api.us-east-1.amazonaws.com/default/api/data",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
        },
        body: JSON.stringify(newUserData),
      }
    );

    if (!response.ok) {
      console.error("Error creating user:", await response.text());
      return;
    }

    const newUser = await response.json();
    console.log("New user created:", newUser);
  } catch (error) {
    console.error("Error creating user:", error);
  }
};

// Update an existing user in Lambda
export const updateUser = async (
  _id: string,
  formData: UserUpdateData
): Promise<void> => {
  try {
    const response = await fetch(
      `https://njzudhkqwg.execute-api.us-east-1.amazonaws.com/default/api/data/${_id}`,
      {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
        },
        body: JSON.stringify(formData),
      }
    );

    if (!response.ok) {
      console.error("Error updating user:", await response.text());
      return;
    }

    const updatedUser = await response.json();
    console.log("User updated:", updatedUser);
  } catch (error) {
    console.error("Error updating user:", error);
  }
};

// Delete a user from Lambda
export const deleteUser = async (_id: string): Promise<void> => {
  try {
    const response = await fetch(
      `https://njzudhkqwg.execute-api.us-east-1.amazonaws.com/default/api/data/${_id}`,
      {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
        },
      }
    );

    if (!response.ok) {
      console.error("Error deleting user:", await response.text());
      return;
    }

    console.log(`User with ID: ${_id} deleted.`);
  } catch (error) {
    console.error("Error deleting user:", error);
  }
};
