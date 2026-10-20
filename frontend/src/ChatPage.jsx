import { Navigate, useParams } from "react-router-dom";
import ChatInterface from "./components/ChatInterface";

const assistants = {
  hr: { name: "People & HR", tone: "violet", topics: "people policies, benefits, hiring, and workplace support", prompts: ["How do I get started?", "Where can I find a people policy?", "Who can help with benefits?"] },
  employee: { name: "Employee", tone: "blue", topics: "workplace tools, everyday processes, and employee support", prompts: ["How do I get started?", "Where can I find a company policy?", "Who can help me with a request?"] },
  finance: { name: "Finance", tone: "amber", topics: "expenses, budgets, invoices, and finance processes", prompts: ["How do I submit an expense?", "Where can I find finance guidance?", "Who can help with an invoice?"] },
  c_level: { name: "Executive", tone: "mint", topics: "leadership priorities, company planning, and business operations", prompts: ["What can you help me with?", "Where can I find planning guidance?", "How do I get started?"] },
};

export default function ChatPage() {
  const { role } = useParams();
  const assistant = assistants[role];
  if (!assistant) return <Navigate to="/dashboard" replace />;
  return <ChatInterface assistant={assistant} />;
}
