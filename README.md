# TAMUevent

## Overview

[TAMUevent](tamuevent.com) is a full-stack web application that helps Texas A&M students and visitors discover upcoming campus events. It combines an automated web scraper, a database with vector-based search capabilities, and a conversational interface to make finding events more intuitive and interactive.

The system is built using a Flask backend, a React frontend, and a PostgreSQL database. It continuously updates event data from official sources and supports semantic and keyword-based event searches through a chatbot-style interface.

## Features
### Event Data Management

Automatically scrapes events from the [Texas A&M University calendar](https://calendar.tamu.edu/) and [Event Registration System](https://ers.tamu.edu/).

Uses a two-table swapping system (eventsA and eventsB) to ensure uninterrupted service during data updates.

Integrates with PostgreSQL and combines full-text search and vector similarity for fuzzy event searching.

### Conversational Search

A chat-based frontend built with [Deep-Chat](https://github.com/OvidijusParsiunas/deep-chat.git) allows users to describe what they are looking for in natural language.

Returns a ranked list of events that best match the query.

Example prompt: “What events related to building a good resume are coming up in the future?”

### Backend

Provides REST endpoints for chatbot queries and data scraping.

Uses a JSON metadata file to track the currently active data table.

Designed to run continuously with background scheduling for updates.

### Frontend

Built with React and designed for simplicity and responsiveness.

Includes a chatbot component that interacts directly with the Flask API.

Built assets can be served by any static web server (currently deploying on Nginx).

### Deployment

Designed for Linux-based cloud environments and deployed on Google Cloud Platform.

Flask application runs under process management (PM2) for reliability.

Supports HTTPS configuration and reverse proxy routing through Nginx.