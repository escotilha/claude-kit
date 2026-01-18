# PRD: Agent Chat Tab

## Overview

Add a "Chat" tab as the FIRST tab in the agent detail page at `/agents/[id]`. This provides users with a proper chat interface to interact with their deployed agents directly from the agent management page.

## Goals

- Provide users with an intuitive way to chat with their deployed agents
- Store conversation history in the database for future reference
- Support file uploads for document-based conversations
- Replace "Test Console" terminology with agent-focused naming

## Non-Goals

- Building a separate chat application (this is embedded in the agent detail page)
- Real-time streaming responses (using request/response model)
- Multi-user conversations or sharing

## User Stories

### US-001: Add Chat Tab to Agent Detail Page

**Description:** As a user, I want to see a "Chat" tab as the first tab in my agent detail page so that I can easily find and use the chat interface.

**Acceptance Criteria:**

- [ ] Chat tab appears as the first tab (before Overview)
- [ ] Tab uses MessageSquare icon
- [ ] Tab label is "Chat"
- [ ] Default tab for deployed agents is Chat (instead of Getting Started)
- [ ] Typecheck passes

### US-002: Create Agent Chat Component with Messages Panel

**Description:** As a user, I want a chat component with a conversation history sidebar and main chat area so that I can manage multiple conversations with my agent.

**Acceptance Criteria:**

- [ ] Left sidebar shows "Quick Messages" section with preset messages
- [ ] Preset messages include: "Hello", "Help me with...", "What can you do?", "Show an example"
- [ ] "Add Custom" button allows creating custom preset messages
- [ ] "Conversation History" section shows past conversations
- [ ] Main chat area shows agent name and description
- [ ] Chat area has "Clear" and "New" buttons in header
- [ ] Typecheck passes

### US-003: Implement Chat Input with File Upload

**Description:** As a user, I want to send messages and attach files so that I can have document-based conversations with my agent.

**Acceptance Criteria:**

- [ ] Message input field with placeholder text
- [ ] Paperclip icon button for file attachments
- [ ] Send button to submit messages
- [ ] Files upload via /api/documents/upload
- [ ] Uploaded files show as chips with remove option
- [ ] Enter key sends message
- [ ] Typecheck passes

### US-004: Create Conversations API Endpoints

**Description:** As a developer, I want API endpoints to manage chat conversations so that the frontend can persist and retrieve conversation history.

**Acceptance Criteria:**

- [ ] GET /api/agents/[agentId]/conversations - lists conversations
- [ ] POST /api/agents/[agentId]/conversations - creates new conversation
- [ ] GET /api/agents/[agentId]/conversations/[conversationId] - gets messages
- [ ] DELETE /api/agents/[agentId]/conversations/[conversationId] - deletes conversation
- [ ] Endpoints check agent ownership/team membership
- [ ] Typecheck passes

### US-005: Integrate Runtime Chat Endpoint

**Description:** As a user, I want my messages to be sent to my deployed agent and receive responses so that I can have real conversations.

**Acceptance Criteria:**

- [ ] POST to /api/runtime/agents/[agentId]/chat with message payload
- [ ] Payload includes: message, messages (history), documentIds
- [ ] Response displays in chat area
- [ ] Loading state shown while waiting for response
- [ ] Error states handled gracefully
- [ ] Typecheck passes

### US-006: Store Conversation History in Database

**Description:** As a user, I want my conversations saved to the database so that I can resume them later.

**Acceptance Criteria:**

- [ ] User messages stored in TestMessage table with role USER
- [ ] Agent responses stored with role ASSISTANT
- [ ] Token usage and latency captured
- [ ] Conversations linked to agent and user
- [ ] Conversations persist across page reloads
- [ ] Typecheck passes

### US-007: Rename Test Console Labels

**Description:** As a user, I want the chat interface to show my agent's name instead of "Test Console" terminology so that the interface feels production-ready.

**Acceptance Criteria:**

- [ ] Chat header shows agent name instead of "Test Console"
- [ ] Remove "Testing:" prefix from any labels
- [ ] Empty state shows "Send a message to chat with [agent name]"
- [ ] Typecheck passes

### US-008: Quick Messages Panel Functionality

**Description:** As a user, I want to click on quick messages to send them instantly so that common interactions are faster.

**Acceptance Criteria:**

- [ ] Clicking a quick message populates the input
- [ ] Quick messages stored in localStorage per agent
- [ ] Custom quick messages can be added via "Add Custom" button
- [ ] Custom quick messages can be removed
- [ ] Typecheck passes

## Technical Approach

1. **New Component**: Create `AgentChat` component in `src/components/agent/agent-chat.tsx`
2. **Reuse Patterns**: Follow the pattern from `src/components/interview/chat.tsx` and `InputArea`
3. **API Layer**: Create conversation management endpoints in `src/app/api/agents/[id]/conversations/`
4. **Database**: Use existing `TestConversation` and `TestMessage` models (already have right schema)
5. **State Management**: Use React Query for conversation list and TanStack Query for caching
6. **File Upload**: Reuse existing document upload infrastructure

## Success Metrics

- Users can successfully chat with deployed agents from the agent detail page
- Conversation history persists and can be resumed
- File attachments work correctly in conversations
- No "test" or "testing" terminology visible to users

## Dependencies

- US-004 must be completed before US-006 (API endpoints needed for storage)
- US-003 depends on US-002 (input is part of chat component)
- US-005 depends on US-003 (need input to send messages)
