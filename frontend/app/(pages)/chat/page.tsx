"use client";

import { Input } from "@/components/ui/input";
import { Message, messageSchema } from "@/schema";
import { useState} from "react";
import chat from "@/actions/chat";
import { Button } from "@/components/ui/button";

function UserMessage({ content }: { content: string }) {
  return (
      <div className="bg-[--foreground] text-black p-4 rounded-lg">{content}</div>
  );
}

function AssistantMessage({ content }: { content: string }) {
  return (
      <div className="bg-[--foreground] text-black p-4 rounded-lg">{content}</div>
  );
}

function MessageListItem({ message }: { message: Message }) {
  return message.role === "user" ? (
      <UserMessage content={message.content} />
  ) : (
      <AssistantMessage content={message.content} />
  );
}

function MessageList({ messages }: { messages: Message[] }) {
  return (
      <div className="py-2">
          {messages.map((message, index) => (
              <MessageListItem key={index} message={message} />
          ))}
      </div>
  );
}

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState("");
  const [botMessages, setBotMessage] = useState<Message[]>([]);
  
  const handleSubmit = async () => {
     let currentMessages: Message[] = messages;
     const newMessage = messageSchema.parse({ content: inputValue, role: "user" });
     setMessages([...currentMessages, newMessage]);
     currentMessages = [...currentMessages, newMessage];
     let response: Message = await chat(newMessage)
     const newBotMessage = messageSchema.parse({ content: response.content, role: "assistant" });
     setBotMessage([...botMessages,newBotMessage]);
     setInputValue("");
  }
  const clearChat = () => {
    setMessages([]);
    setBotMessage([]);
    setInputValue("");
  }
  return (
    <div className="flex flex-col h-screen justify-center items-center w-full"> 
    <div className="flex flex-col">
       <MessageList messages={messages}/>
        <MessageList messages={botMessages}/>
    </div>
    <div className="w-1/2">
        <Input placeholder="Type your message" value={inputValue} onChange={(e) => setInputValue(e.target.value)}/></div>
       <div className="flex flex-row py-2 gap-2">
        <Button onClick={handleSubmit}>Send</Button>
        <Button onClick={clearChat}>Clear</Button></div>
    </div>
  );
}
