# Personal PS5 Payloads List

Your own payload catalog (`payloads.json`) for the **PS5 Payload Manager (`pldmgr`)**. You list GitHub repositories in `repos.txt`, and a GitHub Action picks the `.elf`/`.bin` file from each one's latest release and rebuilds the catalog every 6 hours. The catalog is served through GitHub Pages.

## Setup

1. **Fork** this repository.
2. In your fork, open the **Actions** tab and enable workflows.
3. **Settings → Actions → General → Workflow permissions**: select **Read and write permissions**.
4. **Settings → Pages**: choose **Deploy from a branch**, `main`, `/ (root)`.

## Adding payloads

### Using the page

1. Create a [Fine-Grained Token](https://github.com/settings/personal-access-tokens/new) with access to **only your fork** and the **Contents: Read and write** permission.
2. Open `https://YOUR-USER.github.io/personal-ps5-payloads-list/`, paste the token into **GitHub token** and click **Save**.
3. Paste a repository URL into **Add repository**, click **Check**, then click **Add to repos.txt**.

Visitors without a token can only view the page.

### Manually

1. Edit `repos.txt` in your fork and add one repository per line (`https://github.com/owner/repo` or `owner/repo`).
2. Commit to `main`. The Action runs automatically and updates `payloads.json`.

Either way, the new payload shows up in `payloads.json` within a few minutes. The repository needs a release with a `.elf` or `.bin` file.

## Using it in the PS5 Payload Manager

In the Payload Manager, add this URL as a catalog source:

```
https://YOUR-USER.github.io/personal-ps5-payloads-list/payloads.json
```

The page also shows this URL with a **Copy** button. Whenever a tracked repository publishes a new release, the catalog picks it up automatically.
