# Product Generator - Image Path Auto-Generation

## How It Works

When you type a product name, the generator automatically creates:

### Example: "Premium Cotton Bedsheet"

**Product ID:** 6 (auto-detected)
**Slug:** premium-cotton-bedsheet (auto-generated)

**Main Image Path:**
```
images/products/6-premium-cotton-bedsheet/6-premium-cotton-bedsheet-main.jpg
```

**Gallery Images (6 images by default):**
```
images/products/6-premium-cotton-bedsheet/6-premium-cotton-bedsheet-1.jpg
images/products/6-premium-cotton-bedsheet/6-premium-cotton-bedsheet-2.jpg
images/products/6-premium-cotton-bedsheet/6-premium-cotton-bedsheet-3.jpg
images/products/6-premium-cotton-bedsheet/6-premium-cotton-bedsheet-4.jpg
images/products/6-premium-cotton-bedsheet/6-premium-cotton-bedsheet-5.jpg
images/products/6-premium-cotton-bedsheet/6-premium-cotton-bedsheet-6.jpg
```

## Features

✅ **Auto-Generation:** Paths are automatically generated as you type the product name
✅ **Editable:** All paths can be manually edited after generation
✅ **Dynamic:** Click "+ Add Image" to add more gallery images (auto-numbered)
✅ **Removable:** Click "Remove" on any gallery image to delete it
✅ **Folder Structure:** Each product gets its own folder: `{id}-{slug}/`
✅ **Consistent Naming:** `{id}-{slug}-{number}.jpg` format

## Folder Structure Created

```
images/
└── products/
    └── 6-premium-cotton-bedsheet/
        ├── 6-premium-cotton-bedsheet-main.jpg
        ├── 6-premium-cotton-bedsheet-1.jpg
        ├── 6-premium-cotton-bedsheet-2.jpg
        ├── 6-premium-cotton-bedsheet-3.jpg
        ├── 6-premium-cotton-bedsheet-4.jpg
        ├── 6-premium-cotton-bedsheet-5.jpg
        └── 6-premium-cotton-bedsheet-6.jpg
```

## Usage

1. Type product name → Paths auto-generate
2. Edit any path if needed
3. Click "+ Add Image" for more images
4. Click "Remove" to delete any gallery image
5. Generate JSON with properly formatted image paths
