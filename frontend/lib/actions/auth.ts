"use server";
import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";

import { createBrowserClient } from "@/utils/supabase/client";

// Define a type for the input parameters
type AuthData = {
  email: string;
  password: string;
};

export async function login({ email, password }: AuthData) {
  const supabase = createBrowserClient();

  // Ensure that email and password are strings and not empty
  if (
    typeof email !== "string" ||
    typeof password !== "string" ||
    !email ||
    !password
  ) {
    // Redirect or handle the error appropriately
    throw new Error("Please fill in both email and password");
  }

  const { error } = await supabase.auth.signInWithPassword({ email, password });

  if (error) {
    throw new Error(error.message);
  }

  revalidatePath("/", "page");
  redirect("/menu");
}

export async function signup({ email, password }: AuthData) {
  const supabase = createBrowserClient();

  // Ensure that email and password are strings and not empty
  if (
    typeof email !== "string" ||
    typeof password !== "string" ||
    !email ||
    !password
  ) {
    // Redirect or handle the error appropriately
    throw new Error("Please fill in both email and password");
  }

  const { data, error } = await supabase.auth.signUp({ email, password });
  if (error) {
    throw new Error(error.message);
  }

  console.log(data);
  revalidatePath("/", "page");
  redirect("/auth");
}