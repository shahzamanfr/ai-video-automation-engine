<<<<<<< HEAD
# Stoic AI Short-Form Video Automation

An end-to-end AI content generation pipeline built with n8n.

This system:

- Generates stoic stories using LLM
- Converts script to voiceover using Kokoro TTS
- Creates AI-generated images via deAPI (Flux model)
- Auto-generates SRT captions synced with narration
- Composes final MP4 video via Python server
- Stores metadata in Google Sheets
- Uploads assets to Google Drive

## Architecture

Schedule Trigger
→ LLM Story Generator
→ Description Generator
→ Image Prompt Generator
→ deAPI Image Creation
→ TTS Voiceover
→ Caption Generator
→ Video Composer
→ Google Drive + Sheets Logging

## Stack

- n8n
- OpenRouter (Mistral 7B)
- deAPI (Flux1schnell)
- Kokoro TTS
- Python Video Renderer
- Google Drive API
- Google Sheets API

## Purpose

Automated faceless YouTube Shorts pipeline focused on stoic philosophy and ancient Rome themes.

Fully automated every 2 hours.
=======
# ai-video-automation-engine
End-to-end AI video automation pipeline using LLMs, image generation, TTS, caption syncing, and programmatic video rendering with n8n orchestration.
>>>>>>> c88053f62266b766d403ebf23539249441e8c994
