"use server"
import { Message } from "../schema";


async function chat(message: Message) {
    try {
        const response = await fetch(`http://localhost:8000/chat`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(message)
        });
        if (response.ok) {
            return response.json();
        }

    } catch (error) {
        console.log("The Error is " + error + " code:  ");
    }
   
}

export default chat;