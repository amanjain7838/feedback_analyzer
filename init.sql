-- Create feedback table
CREATE TABLE feedback (
    id SERIAL PRIMARY KEY,
    source VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sentiment VARCHAR(20),
    category VARCHAR(100)
);

-- Create index for time-based queries
CREATE INDEX idx_feedback_created_at ON feedback(created_at DESC);
CREATE INDEX idx_feedback_sentiment ON feedback(sentiment);

-- Seed with realistic feedback data
INSERT INTO feedback (source, content, created_at, sentiment, category) VALUES
('app_store', 'The app crashes every time I try to export my data. Very frustrating after paying for premium. Please fix this ASAP!', NOW() - INTERVAL '2 days', 'negative', 'bugs'),
('support_ticket', 'Love the new dark mode! However, I noticed the search feature is slower than before. Takes 3-4 seconds to return results now.', NOW() - INTERVAL '1 day', 'mixed', 'performance'),
('survey', 'The onboarding experience was smooth and intuitive. I was able to set up my account in under 5 minutes. Great job!', NOW() - INTERVAL '3 days', 'positive', 'onboarding'),
('app_store', 'Been using this for 6 months. Solid app but really needs multi-user support. My team can''t collaborate effectively without it.', NOW() - INTERVAL '5 days', 'mixed', 'feature_request'),
('support_ticket', 'Payment failed multiple times with my credit card. Had to use PayPal instead. Not sure if this is a known issue?', NOW() - INTERVAL '1 day', 'negative', 'payments'),
('survey', 'The mobile app is fantastic, but the desktop version feels outdated. Would love to see feature parity between platforms.', NOW() - INTERVAL '4 days', 'mixed', 'platform'),
('app_store', 'Best productivity app I''ve used! The UI is clean and everything just works. Worth every penny.', NOW() - INTERVAL '2 days', 'positive', 'general'),
('support_ticket', 'Cannot sync my data across devices. Tried logging out and back in but the problem persists. Using iPhone 14 and MacBook Pro.', NOW() - INTERVAL '6 hours', 'negative', 'sync'),
('survey', 'Integration with Google Calendar works perfectly. Saves me so much time. One suggestion: add Outlook integration too?', NOW() - INTERVAL '1 day', 'positive', 'integrations'),
('app_store', 'App is way too expensive compared to competitors. $15/month is hard to justify when alternatives are $5-8.', NOW() - INTERVAL '3 days', 'negative', 'pricing'),
('support_ticket', 'The new release (v2.3) fixed the notification bug I reported last week. Thank you for the quick turnaround!', NOW() - INTERVAL '12 hours', 'positive', 'bugs'),
('survey', 'I wish there was a way to customize the dashboard. Everyone''s workflow is different and rigid layouts don''t work for me.', NOW() - INTERVAL '2 days', 'mixed', 'customization'),
('app_store', 'Constant notifications are annoying. I turned them off but still get in-app popups. Please respect user preferences!', NOW() - INTERVAL '4 days', 'negative', 'notifications'),
('support_ticket', 'File upload size limit of 10MB is too small. I work with large design files and can''t attach them to tasks.', NOW() - INTERVAL '1 day', 'negative', 'limitations'),
('survey', 'Customer support responded within an hour and solved my issue. Really impressed with the service level.', NOW() - INTERVAL '5 days', 'positive', 'support'),
('app_store', 'Good app but battery drain is significant. Goes from 100% to 50% in 3 hours of active use. iPhone 13 Pro.', NOW() - INTERVAL '2 days', 'mixed', 'performance'),
('support_ticket', 'Tried to cancel my subscription but couldn''t find the option in settings. Had to email support. Make this clearer please.', NOW() - INTERVAL '3 days', 'negative', 'ux'),
('survey', 'The keyboard shortcuts are a game changer for power users. Documentation could be better though.', NOW() - INTERVAL '1 day', 'positive', 'features'),
('app_store', 'Decent app but feels unpolished. Lots of small UI glitches and inconsistent styling throughout.', NOW() - INTERVAL '6 days', 'mixed', 'ui'),
('support_ticket', 'Search doesn''t find items I know exist. Seems like it only searches titles and not content? Very limiting.', NOW() - INTERVAL '8 hours', 'negative', 'search'),
('survey', 'Offline mode works great! I can keep working on the plane and everything syncs when I land.', NOW() - INTERVAL '4 days', 'positive', 'offline'),
('app_store', 'Latest update broke the widget. It just shows a blank screen now. Please roll back or fix urgently!', NOW() - INTERVAL '1 day', 'negative', 'bugs'),
('support_ticket', 'Would love to see a bulk edit feature. Currently have to update 50+ items one by one which takes forever.', NOW() - INTERVAL '2 days', 'mixed', 'feature_request'),
('survey', 'The learning curve was steeper than expected. More video tutorials would help new users get started.', NOW() - INTERVAL '5 days', 'mixed', 'onboarding'),
('app_store', 'Five stars! This app has completely changed how I manage my projects. Can''t imagine going back to my old tools.', NOW() - INTERVAL '3 days', 'positive', 'general'),
('support_ticket', 'API rate limits are too restrictive for our use case. We need at least 1000 requests/hour, currently capped at 100.', NOW() - INTERVAL '1 day', 'negative', 'api'),
('survey', 'Love the template library! Saved me hours of setup time. More industry-specific templates would be awesome.', NOW() - INTERVAL '6 days', 'positive', 'templates'),
('app_store', 'App freezes when scrolling through long lists. Seems like a memory leak or poor optimization.', NOW() - INTERVAL '2 days', 'negative', 'performance'),
('support_ticket', 'The recent redesign looks modern but I miss some of the old features. Is there a way to switch to classic view?', NOW() - INTERVAL '4 days', 'mixed', 'ui'),
('survey', 'Collaboration features work well but real-time updates lag sometimes. Would be nice to see who''s viewing what.', NOW() - INTERVAL '1 day', 'mixed', 'collaboration');