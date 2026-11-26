# Personal PS5 Payloads List

Your own payload catalog (`payloads.json`) for the **PS5 Payload Manager (`pldmgr`)**. You add GitHub repositories to the `repos/` folder, and a GitHub Action picks the `.elf`/`.bin` file from each one's latest release and rebuilds the catalog every 6 hours. The catalog is served through GitHub Pages.

## Setup

1. **Fork** this repository.
2. In your fork, open the **Actions** tab and enable workflows.
3. **Settings → Actions → General → Workflow permissions**: select **Read and write permissions**.
4. **Settings → Pages**: choose **Deploy from a branch**, `main`, `/ (root)`.

## Adding payloads

### Using the page

1. Create a [Fine-Grained Token](https://github.com/settings/personal-access-tokens/new) with access to **only your fork** and the **Contents: Read and write** permission.
2. Open `https://YOUR-USER.github.io/personal-ps5-payloads-list/manage/`, paste the token into **GitHub token** and click **Save**. You only do this once per browser. The token stays saved until it expires or you remove it.
3. Paste one or more repository URLs (one per line) into **Add repositories**, click **Check**, then **Add**. All of them are saved in a single commit.

Without a token, the page is read-only.

### Manually

Create a file in the `repos/` folder (for example `owner__repo.txt`) containing the repository URL, `https://github.com/owner/repo`. A single file can also list several repositories, one per line. Commit to `main` and the Action updates `payloads.json`.

Either way, the new payload shows up in `payloads.json` within a few minutes. The repository needs a release with a `.elf` or `.bin` file.

## Using it in the PS5 Payload Manager

In the Payload Manager, add this URL as a catalog source:

```
https://YOUR-USER.github.io/personal-ps5-payloads-list/payloads.json
```

The page also shows this URL with a **Copy** button. Whenever a tracked repository publishes a new release, the catalog picks it up automatically.
