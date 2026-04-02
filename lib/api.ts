import { Attendee, MicroCircle, Connection, FollowUp, Notification, Event } from "./types";

const MOCK_ATTENDEES: Attendee[] = [
  {
    id: "nina",
    name: "Nina Patel",
    role: "Healthcare AI Lead",
    company: "Tempus AI",
    avatar: "https://i.pravatar.cc/150?u=nina",
    matchScore: 92,
    serendipityScore: 88,
    bio: "Building the future of precision medicine with generative AI. Former researcher at Stanford.",
    skills: ["AI/ML", "Healthcare", "Python", "Product", "Data Strategy"],
    interests: ["Longevity", "Precision Medicine", "Ethics", "Tennis"],
    matchReason: "Shared focus on Healthcare AI & ethics-driven models.",
    warmPath: ["You", "Sam Chen", "Nina Patel"],
    transcript: "We discussed the challenges of dataset bias in clinical LLMs."
  },
  {
    id: "sam",
    name: "Sam Chen",
    role: "Founder",
    company: "Nexus Labs",
    avatar: "https://i.pravatar.cc/150?u=sam",
    matchScore: 85,
    serendipityScore: 78,
    bio: "Scaling the infrastructure for decentralized intelligence.",
    skills: ["Blockchain", "Infrastructure", "Pitching", "Hiring"],
    interests: ["Web3", "Robotics", "Sailing"],
    matchReason: "Sam bridged your connection to 3 potential investors."
  },
  {
    id: "rhea",
    name: "Rhea Kapur",
    role: "VP of Engineering",
    company: "Carbon One",
    avatar: "https://i.pravatar.cc/150?u=rhea",
    matchScore: 78,
    serendipityScore: 82,
    bio: "Optimizing supply chains for carbon neutrality.",
    skills: ["Supply Chain", "Optimization", "Scale", "Hiring"],
    interests: ["Climate Tech", "Hiking"],
    matchReason: "Shared interest in Climate Tech and Scale."
  }
];

export const KindredAPI = {
  getCurrentEvent: async (): Promise<Event> => ({
    id: "hack-chi-3",
    name: "HackWithChicago 3.0",
    date: "April 2, 2026",
    location: "Chicago, IL",
  }),

  getRecommendations: async (): Promise<Attendee[]> => MOCK_ATTENDEES,

  getAttendee: async (id: string): Promise<Attendee | undefined> => 
    MOCK_ATTENDEES.find(a => a.id === id),

  getMicroCircles: async (): Promise<MicroCircle[]> => [
    {
      id: "circle-1",
      attendees: [MOCK_ATTENDEES[0], MOCK_ATTENDEES[1], MOCK_ATTENDEES[2]],
      loopName: "Funding Loop",
      flowDescription: "You offer AI Expertise → Sam offers Investor Intros → Rhea offers GTM Strategy"
    }
  ],

  getConnections: async (): Promise<Connection[]> => [
    {
      id: "conn-1",
      attendee: MOCK_ATTENDEES[0],
      timestamp: "2h ago",
      summary: "Discussed clinical trials and data bias.",
      followupStatus: "pending"
    }
  ],

  getFollowUps: async (): Promise<FollowUp[]> => [
    {
      id: "fw-1",
      attendee: MOCK_ATTENDEES[0],
      discussedTopic: "Clinical trial dataset sharing",
      suggestedAction: "Share deck",
      deadline: "2 days left"
    }
  ],

  getNotifications: async (): Promise<Notification[]> => [
    { id: "n1", type: "match", text: "New high-serendipity match found: Nina Patel", timestamp: "2m ago", relatedId: "nina" },
    { id: "n2", type: "proximity", text: "Priya is nearby — 5m away", timestamp: "10m ago" },
    { id: "n3", type: "followup", text: "Follow up with Alex — 2 days left", timestamp: "1h ago" }
  ]
};
