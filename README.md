# Calendar Events

A simple web application for publishing and subscribing to calendar events. With this website, users can easily keep track of upcoming events and subscribe to the calendar using their preferred calendar client.

## Features

- View a list of upcoming events  
- Export calendar as an iCal (.ics) feed  
- Subscribe to events from Google Calendar, Apple Calendar, Outlook, or any app that supports iCal

## Usage

- Browse the homepage to see a list of upcoming events.
- Click on any event for more details.

## Sankashti Chaturthi calendar (Netherlands time), 2025–2030

All events are in **Netherlands time (Europe/Amsterdam)**. Summer time (CEST) and winter time (CET) are handled automatically. Each event covers the Chaturthi tithi from start to end. The description also gives:

- the **Sankashti day in the Netherlands**, which is the day Chaturthi is in effect at moonrise
- the **moonrise time in Amsterdam**, when the fast is traditionally broken

| File | Contents |
|---|---|
| [`Sankashti_Chaturthi_Netherlands.ics`](Sankashti_Chaturthi_Netherlands.ics) | **All years 2025–2030 in one calendar (recommended)** |
| `Sankashti_Chaturthi_2025.ics` … `Sankashti_Chaturthi_2030.ics` | One calendar per year |

**Where the data comes from:** 2025–2027 use the tithi times from [Drik Panchang](https://www.drikpanchang.com/vrats/sankashti-chaturthi-dates.html). 2028–2030 were calculated astronomically, since the Chaturthi tithi depends only on the Sun–Moon angle. The same method reproduces the Drik Panchang times for 2025–2027 to within a few minutes. A few dates have no single clear Sankashti day in the Netherlands; those events include a note and are worth checking against a local panchang.

## How to Subscribe to This Calendar

### 1. The subscription link

```
https://mohini123.github.io/calendar-events/Sankashti_Chaturthi_Netherlands.ics
```

For iPhone/iPad, the same link starting with `webcal://` opens the Subscribe dialog directly:

```
webcal://mohini123.github.io/calendar-events/Sankashti_Chaturthi_Netherlands.ics
```

(GitHub Pages must be enabled for this repository: **Settings → Pages → Deploy from branch → `main` / root**.)

### 2. Add it to your phone

#### iPhone / iPad

1. Open **Settings → Apps → Calendar → Calendar Accounts → Add Account → Other → Add Subscribed Calendar**. On older iOS versions this is **Settings → Calendar → Accounts**.
2. Paste the link above and tap **Next**, then **Save**.

#### Android (Google Calendar)

The Google Calendar phone app can't add a calendar by URL, so do it once on the web:

1. On a computer, open [Google Calendar](https://calendar.google.com/). Next to **Other calendars**, click **+** → **From URL**.
2. Paste the link and click **Add calendar**.
3. On your phone, open Google Calendar → **Settings** → the new calendar, and make sure **Sync** is on.

### 3. Other calendar apps

#### Google Calendar

1. Open [Google Calendar](https://calendar.google.com/).
2. On the left, click the **+** next to “Other calendars” and select **From URL**.
3. Paste the calendar URL and click **Add calendar**.

#### Apple Calendar (macOS/iOS)

1. Open the Calendar app.
2. Go to **File > New Calendar Subscription**.
3. Paste the calendar URL and click **Subscribe**.

#### Microsoft Outlook

1. Go to **File > Account Settings > Account Settings**.
2. Under the **Internet Calendars** tab, click **New**.
3. Paste the calendar URL and click **Add**.

### 4. Done!

- The calendar events will now sync automatically with your chosen app.

## Contributing

Pull requests and suggestions are welcome!

## License

[MIT](LICENSE)
