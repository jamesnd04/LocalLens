"use client";
import React from "react";
import LoginForm  from "@/components/login-form";
import { useRouter } from "next/navigation";
import { SignupForm } from "@/components/signup-form";

export default function Authentication() {
    return ( 
        <div>
        <div className="flex flex-col h-screen justify-center items-center py-16">
        <div className="items-center">
            <LoginForm />
        </div>
        </div>
        </div>
    )}
  
    