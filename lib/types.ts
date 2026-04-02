export type Attendee = {
  id: string;
  name: string;
  role: string;
  company: string;
  avatar: string;
  matchScore: number;
  serendipityScore: number;
  bio?: string;
  skills: string[];
  interests: string[];
  matchReason?: string;
  warmPath?: string[];
  transcript?: string;
};

export type MicroCircle = {
  id: string;
  attendees: Attendee[];
  loopName: string;
  flowDescription: string;
};

export type Connection = {
  id: string;
  attendee: Attendee;
  timestamp: string;
  summary: string;
  followupStatus: 'pending' | 'done';
};

export type FollowUp = {
  id: string;
  attendee: Attendee;
  discussedTopic: string;
  suggestedAction: string;
  deadline: string;
};

export type Notification = {
  id: string;
  type: 'match' | 'proximity' | 'followup' | 'system';
  text: string;
  timestamp: string;
  relatedId?: string;
};

export type Event = {
  id: string;
  name: string;
  date: string;
  location: string;
  imageUrl?: string;
};
