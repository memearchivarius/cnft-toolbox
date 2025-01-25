# Compressed NFT Processing

## Introduction

cNFT, or compressed NFT, is a specialized digital asset format that optimizes data storage. By employing data
compression algorithms, cNFT reduces file sizes without compromising uniqueness, thereby saving space on servers and
reducing data storage and transmission costs. Merkle trees play a crucial role in enhancing the efficiency of cNFT
collections by minimizing storage requirements.

## Features

- **Resource Savings**: Use Merkle trees to store only essential data, reducing gas costs and network load.
- **Improved Scalability**: Design efficient contracts that handle large NFT volumes without performance loss.
- **Optimized Data Storage**: Keep minimal on-chain info to boost system responsiveness and save space.
- **Enhanced Security**: Employ Merkle trees for quick data integrity checks and robust asset protection.
- **Cost Reduction**: Shift minting costs to end-users and create “virtual” items on-chain only when needed.

## Supporting Compressed NFT in Wallets and Marketplaces

* **Current Limitations**

  At the time of writing, most popular wallets and marketplaces do not display unclaimed cNFTs or cNFTs from collections
  that are not official partners. The exceptions are the Wallet in Telegram and the Getgems marketplace, which only
  indexes the first 200 items for collections that are not official partners, creating a challenge for larger
  collections.
* **Attack Scenario**

  This limitation stems from a potential attack scenario: a malicious actor can create a collection of hundreds of
  thousands of NFTs at minimal cost, forcing marketplaces to store all related data. Meanwhile, the attacker does not
  even need to host the items themselves-they can simply generate them on demand.
* **Potential Solution**

  A potential solution is to provide a dedicated interface where users can claim their cNFTs. Once claimed, all NFTs are
  indexed and displayed in wallets and marketplaces in a standard manner, ensuring visibility and accessibility.

## Configuration and Deployment Guide

### NFT Collection and Item Preparation

You will need to prepare both the metadata and images for your NFTs. Metadata is the information that describes an NFT
or a collection, and the images will be displayed in the NFT interface.

##### Metadata Preparation

* **Collection Metadata**

  Create a `collection.json` file containing the fields specified in
  the [standard](https://github.com/ton-blockchain/TEPs/blob/master/text/0064-token-data-standard.md#nft-collection-metadata-example-offchain).

  Example:
    ```json
  {
      "name": "<collection name>",
      "description": "<collection description>",
      "image": "<link to the image (e.g. https://yourdomain.com/logo.png)>"
  }
    ```

* **NFT Item Metadata**

  For each NFT, create a separate `.json` file (e.g., `0.json`, `1.json`, etc.) with the fields listed in
  the [standard](https://github.com/ton-blockchain/TEPs/blob/master/text/0064-token-data-standard.md#nft-item-metadata-example-offchain).

  Example:
    ```json
  {
      "name": "<item name>",
      "description": "<item description>",
      "image": "<link to the image (e.g. https://yourdomain.com/0.png)>"
  }
    ```

##### Resource Preparation

* **Images**

  Prepare images for the collection (e.g., `logo.png` for the avatar) and for each NFT (e.g., `0.png`, `1.png`, etc.).

* **JSON Files**

  Host your `collection.json` and `N.json` files (where N is the NFT number) in a publicly accessible location (e.g., a
  public repository or server), ensuring each file has a unique URL.

**Note**: Make sure all your `images` and `.json` files can be accessed directly via their URLs.

### TON Connect Manifest Preparation

For the NFT claiming interface, create
a [Ton Connect manifest](https://github.com/ton-blockchain/ton-connect/blob/main/requests-responses.md#app-manifest)
json file describing your application for the wallet to display during the connection process.

Example:

```json
{
  "url": "<app url>",
  "name": "<app name>",
  "iconUrl": "<app icon url>"
}
```

**Note**: Ensure this file is publicly accessible via its URL.

### Owner List Preparation

Prepare an `owners.txt` file listing the addresses of item owners, one per line. The first address corresponds to item
index `0`, the second address to item index `1`, and so on.

Example:

```text
EQAFmjUoZUqKFEBGYFEMbv-m61sFStgAfUR8J6hJDwUU09iT
UQDYzZmfsrGzhObKJUw4gzdeIxEai3jAFbiGKGwxvxHinf4K
UQCDrgGaI6gWK-qlyw69xWZosurGxrpRgIgSkVsgahUtxZR0
```

### Infrastructure Preparation

You also need to set up a server to host your API and the interface for claiming NFTs, as well as obtain a domain for
accessing the API. In this example, we’ll run a local test deployment on a home machine and use ngrok to make it
publicly accessible.

### Claiming API and Interface Setup

Follow these steps to host the API and user interface for claiming NFTs.

1. **Clone the Repository**

    - Make a local copy of the project containing all necessary source files.

      ```bash
      git clone https://github.com/nessshon/cnft-toolbox
      ```

2. **Install Dependencies**

    - Install `docker`, `docker-compose` and `ngrok`, ensuring they’re properly configured on your machine.

3. **Create Telegram Bot**

    - Create a Telegram bot and obtain its API token.

4. **Expose Your API**

    - In this example, `ngrok` is used to create a public URL for testing purposes:
      ```bash
      ngrok http 8080
      ```
    - **For production**, you should set up a custom domain and configure Nginx to proxy requests to your API on port
        8080.
      This involves:
        - Registering a domain and pointing it to your server.
        - Configuring Nginx to proxy requests to your API on port 8080.

5. **Create a `.env` file from the `env.example`:**

    - Duplicate the `env.example` file to `.env` and update it with your specific configuration:

      | **Key**                   | **Description**                                                                                    | **Example**                                      | **Notes**                                                         |
      |---------------------------|----------------------------------------------------------------------------------------------------|--------------------------------------------------|-------------------------------------------------------------------|
      | `PORT`                    | Port on which the API will run.                                                                    | `8080`                                           |                                                                   |
      | `ADMIN_USERNAME`          | The admin username for accessing restricted functionalities.                                       | `admin`                                          |                                                                   |
      | `ADMIN_PASSWORD`          | The admin password for accessing restricted functionalities.                                       | `password`                                       |                                                                   |
      | `DEPTH`                   | Depth for the NFT collection (the maximum number of items is `2^DEPTH`, with a max `DEPTH` of 30). | `20`                                             |                                                                   |
      | `IS_TESTNET`              | Indicates whether you are connecting to the TON testnet (`true`) or mainnet (`false`).             | `true` or `false`                                |                                                                   |
      | `POSTGRES_PASSWORD`       | The password for PostgreSQL authentication.                                                        | `secret`                                         |                                                                   |
      | `POSTGRES_DB`             | The name of the PostgreSQL database.                                                               | `merkleapi`                                      |                                                                   |
      | `POSTGRES_URI`            | The full connection URI for PostgreSQL.                                                            | `postgresql://postgres:secret@db:5432/merkleapi` |                                                                   |
      | `BOT_TOKEN`               | The token for your Telegram bot (from [@BotFather](https://t.me/BotFather)).                       | `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`      | Telegram bot will be used for the NFT claiming interface.         |
      | `API_BASE_URL`            | The external domain of your API.                                                                   | `https://4arw-91-212-28-241.ngrok-free.app`      | Replace with your own public URL (e.g., via ngrok).               |
      | `TONCONNECT_MANIFEST_URL` | URL for the Ton Connect manifest file.                                                             | `https://example.com/tonconnect-manifest.json`   | Replace with the public URL of the manifest file created earlier. |
      | `COLLECTION_ADDRESS`      | Address of the NFT collection.                                                                     |                                                  | Fill this in **after** the collection is deployed.                |

### Run the API and Deploy the Collection

1. **Start the API and Database**

    - Run the following command to start the API and database:
      ```bash
      docker-compose up db api -d
      ```

2. **Migrate the Database**

    - Create the required tables in the database:
      ```bash
      docker-compose exec api /ctl migrate
      ```

3. **Add Owners**

    - Place your `owners.txt` file (containing owners’ addresses) into the `api` folder, then run:

      ```bash
      docker-compose exec api /ctl add /api/owners.txt
      ```

4. **Rediscover Items**

    - In a browser, navigate to: `<API_URI>/admin/rediscover`
    - Use your `ADMIN_USERNAME` and `ADMIN_PASSWORD` to log in.
    - If everything works correctly, you should see `ok` in the browser.
    - A file named `1.json` (or a similarly named file) will appear in the `api/apidata/upd` folder after some time (
      depending on the number of items).

5. **Generate an Update**

    - Run the following command to generate an update:

      ```bash
      docker-compose exec api /ctl genupd <path-to-update-file> <collection-owner> <collection-meta> <item-meta-prefix> <royalty-base> <royalty-factor> <royalty-recipient> <api-uri-including-v1>
      ```

        - **path-to-update-file**: Path to the file created in step 4 (e.g., `api/apidata/upd/1.json`).
        - **collection-owner**: Address of the NFT collection owner.
        - **collection-meta**: Full URL to the collection metadata file. (e.g.,
          `https://yourdomain.com/collection.json`)
        - **item-meta-prefix**: Common prefix for item metadata (e.g., if item 0 has metadata at
          `https://yourdomain.com/0.json`,
          use `https://yourdomain.com/`).
        - **royalty-base**: Numerator for royalties (e.g., `10` for 10% if royalty-factor is 100).
        - **royalty-factor**: Denominator for royalties (e.g., `100` if royalty-base is 10).
        - **royalty-recipient**: Address receiving royalties (can be the same as `<collection-owner>`).
        - **api-uri-including-v1**: Publicly API URL with the `/v1` postfix.

          For example, if you used `https://yourapi.com/admin/rediscover` to generate the update file, you would use
          `https://yourapi.com/v1` here.

6. **Invoke the `ton://` Deeplink**

    - After running the previous command, a `ton://` link should appear in the console logs. Follow the link and confirm
      the transaction.
    - For convenience, you can paste the deeplink into a QR code generator service and scan the generated QR code with
      the Tonhub wallet in either the testnet or mainnet.

7. **Set the Collection Address**

    - In a browser, navigate to: `<API_URI>/admin/setaddr/<collection-address>`

      Where `<collection-address>` is the address you observed after the ton:// deployment step.

8. **Wait for Confirmation**

    - Wait for a `committed state` message in the server logs.

9. **Done!**

### Run the Telegram Bot for NFT Claiming Interface

1. **Update the `.env` File**

    - Add the `COLLECTION_ADDRESS` obtained during the deployment process to your `.env` file.

2. **Start the Telegram Bot**

    - Run the following command to start the Telegram bot:
      ```bash
      docker-compose up redis bot -d
      ```

3. **Interact with the Bot**

    - Open Telegram and navigate to your bot. Follow the instructions provided by the bot to claim NFTs or perform other
      interactions.

4. **Done!**

### Updating Owners

Follow these steps to update the list of owners and integrate the changes into your NFT collection:

1. **Prepare the `new-owners.txt` File**

    - Create a `new-owners.txt` file containing the new owners' addresses. Place this file in the `api` folder.

2. **Add New Owners**

    - Add the new owners to the database by running:
      ```bash
      docker-compose exec api /ctl add /api/new-owners.txt
      ```

3. **Rediscover Items**

    - Navigate to: `<API_URI>/admin/rediscover`
    - Use your `ADMIN_USERNAME` and `ADMIN_PASSWORD` to log in.

4. **Locate the Update File**

    - After rediscovering, locate the new update file in the `api/apidata/upd` folder.  
      *(e.g., `2.json` if the last update was `1.json`.)*

5. **Generate an Update**

    - Run the following command to generate an update:
      ```bash
      docker-compose exec api /ctl genupd <path-to-update-file> <collection-address>
      ```
      Replace:
        - `<path-to-update-file>`: Path to the new update file (e.g., `api/apidata/upd/2.json`).
        - `<collection-address>`: Address of the NFT collection.

6. **Invoke the `ton://` Deeplink**

    - Navigate to the generated `ton://` link and confirm the transaction.
    - For convenience, you can paste the deeplink into a QR code generator service and scan the generated QR code with
      the Tonhub wallet in either the testnet or mainnet.

7. **Wait for Confirmation**

    - Monitor the server logs for a `committed state` message indicating the process is complete.

8. **Done!**

## Conclusion

The Compressed NFT Standard proposes a transformative approach to the creation and management of NFT collections,
offering a scalable, cost-effective solution for mass NFT production. By addressing the limitations of existing
standards, this draft sets the stage for broader adoption and innovative applications of NFT technology in community
building and marketing campaigns.

## See Also

- [Understanding compressed NFT on the TON blockchain](https://ambiguous-mandrill-06a.notion.site/Understanding-compressed-NFT-on-the-TON-blockchain-753ffbcbd1684aef963b5cfb6db93e55)
- [Compressed NFT standard implementation](https://github.com/ton-community/compressed-nft-contract)
- [Reference augmenting API implementation](https://github.com/ton-community/compressed-nft-api)
- [NFT Collection metadata example](https://github.com/ton-blockchain/TEPs/blob/master/text/0064-token-data-standard.md#nft-collection-metadata-example-offchain)
- [NFT Item metadata example](https://github.com/ton-blockchain/TEPs/blob/master/text/0064-token-data-standard.md#nft-item-metadata-example-offchain)
- [Compressed NFT toolbox](https://github.com/nessshon/cnft-toolbox)
