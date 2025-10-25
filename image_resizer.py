"""
Simple Image Resizer - Cross-Platform (Windows & Mac)
Resize images with aspect ratio preservation and web optimization
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk, ImageFilter
import os
from pathlib import Path


class ImageResizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Resizer COED Web Optimizer")
        self.root.geometry("1400x1000")
        self.root.resizable(True, True)
        
        # Variables
        self.original_image = None
        self.original_path = None
        self.preview_image = None
        self.resized_image = None
        self.crop_preview_image = None
        self.keep_aspect_ratio = tk.BooleanVar(value=True)
        self.crop_mode = tk.BooleanVar(value=False)
        self.manual_crop = tk.BooleanVar(value=False)
        self.blur_background = tk.BooleanVar(value=False)
        self.blur_strength = tk.IntVar(value=25)
        self.width_var = tk.StringVar(value="1920")
        self.height_var = tk.StringVar(value="1080")
        self.quality_var = tk.IntVar(value=50)
        self.output_format = tk.StringVar(value="jpg")
        self.needs_crop = False
        self.crop_box = None
        self.manual_crop_offset_x = 0
        self.manual_crop_offset_y = 0
        self.dragging = False
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.crop_interactive_window = None
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        
        # Title with logo
        title_frame = tk.Frame(self.root, bg="#2c3e50", height=60)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        # Try to load logo
        logo_label = None
        try:
            logo_path = "mediaimmagine_logo.png"
            if os.path.exists(logo_path):
                logo_img = Image.open(logo_path)
                logo_img.thumbnail((40, 40), Image.Resampling.LANCZOS)
                logo_photo = ImageTk.PhotoImage(logo_img)
                logo_label = tk.Label(title_frame, image=logo_photo, bg="#2c3e50")
                logo_label.image = logo_photo  # Keep reference
                logo_label.pack(side=tk.LEFT, padx=(10, 10), pady=10)
        except:
            pass
        
        title_label = tk.Label(
            title_frame,
            text="Image Resizer COED Web Optimizer",
            font=("Arial", 18, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(side=tk.LEFT, pady=10)
        
        # Main container with two columns
        main_container = tk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Controls
        left_panel = tk.Frame(main_container, padx=10, pady=10)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
        
        # Right panel - Preview
        right_panel = tk.Frame(main_container, padx=10, pady=10, bg="#f0f0f0", relief=tk.SUNKEN, borderwidth=2)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Setup left panel controls
        self.setup_controls(left_panel)
        
        # Setup right panel preview
        self.setup_preview_panel(right_panel)
    
    def setup_controls(self, parent):
        """Setup the control panel"""
        
        # Upload section
        upload_frame = tk.LabelFrame(parent, text="📁 Upload Image", font=("Arial", 11, "bold"), padx=10, pady=10)
        upload_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.file_label = tk.Label(upload_frame, text="No file selected", fg="gray")
        self.file_label.pack(side=tk.LEFT, padx=5)
        
        upload_btn = tk.Button(
            upload_frame,
            text="Browse...",
            command=self.upload_image,
            bg="#3498db",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=5,
            cursor="hand2"
        )
        upload_btn.pack(side=tk.RIGHT)
        
        # Settings section
        settings_frame = tk.LabelFrame(parent, text="⚙️ Resize Settings", font=("Arial", 11, "bold"), padx=10, pady=10)
        settings_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Dimensions
        dim_frame = tk.Frame(settings_frame)
        dim_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(dim_frame, text="Width:", font=("Arial", 10)).grid(row=0, column=0, sticky=tk.W, padx=5)
        width_entry = tk.Entry(dim_frame, textvariable=self.width_var, width=10, font=("Arial", 10))
        width_entry.grid(row=0, column=1, padx=5)
        width_entry.bind('<KeyRelease>', self.on_width_change)
        
        tk.Label(dim_frame, text="px", font=("Arial", 10)).grid(row=0, column=2, padx=5)
        
        tk.Label(dim_frame, text="Height:", font=("Arial", 10)).grid(row=0, column=3, sticky=tk.W, padx=(20, 5))
        height_entry = tk.Entry(dim_frame, textvariable=self.height_var, width=10, font=("Arial", 10))
        height_entry.grid(row=0, column=4, padx=5)
        height_entry.bind('<KeyRelease>', self.on_height_change)
        
        tk.Label(dim_frame, text="px", font=("Arial", 10)).grid(row=0, column=5, padx=5)
        
        # Aspect ratio checkbox
        aspect_check = tk.Checkbutton(
            settings_frame,
            text="Keep aspect ratio (maintain proportions)",
            variable=self.keep_aspect_ratio,
            font=("Arial", 10),
            command=self.toggle_aspect_ratio
        )
        aspect_check.pack(anchor=tk.W, pady=5)
        
        # Crop mode checkbox
        crop_check = tk.Checkbutton(
            settings_frame,
            text="Crop to fit (when aspect ratio differs)",
            variable=self.crop_mode,
            font=("Arial", 10),
            command=self.toggle_crop_mode
        )
        crop_check.pack(anchor=tk.W, pady=5)
        
        # Manual crop positioning checkbox
        self.manual_crop_check = tk.Checkbutton(
            settings_frame,
            text="Manual crop positioning (drag to adjust)",
            variable=self.manual_crop,
            font=("Arial", 10),
            command=self.toggle_manual_crop,
            state=tk.DISABLED
        )
        self.manual_crop_check.pack(anchor=tk.W, pady=5)
        
        # Blur background checkbox (for vertical to horizontal conversion)
        self.blur_background_check = tk.Checkbutton(
            settings_frame,
            text="Add blur effect on sides (for vertical → horizontal)",
            variable=self.blur_background,
            font=("Arial", 10),
            command=self.toggle_blur_background,
            state=tk.DISABLED
        )
        self.blur_background_check.pack(anchor=tk.W, pady=5)
        
        # Blur strength slider (hidden by default)
        self.blur_strength_frame = tk.Frame(settings_frame)
        
        tk.Label(
            self.blur_strength_frame,
            text="   Blur strength:",
            font=("Arial", 9)
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        blur_slider = tk.Scale(
            self.blur_strength_frame,
            from_=5,
            to=50,
            orient=tk.HORIZONTAL,
            variable=self.blur_strength,
            length=200,
            command=self.on_blur_strength_change
        )
        blur_slider.pack(side=tk.LEFT)
        
        self.blur_strength_label = tk.Label(
            self.blur_strength_frame,
            text="25",
            font=("Arial", 9)
        )
        self.blur_strength_label.pack(side=tk.LEFT, padx=5)
        
        # Crop info label
        self.crop_info_label = tk.Label(
            settings_frame,
            text="",
            font=("Arial", 9, "italic"),
            fg="orange",
            wraplength=380,
            justify=tk.LEFT
        )
        self.crop_info_label.pack(anchor=tk.W, pady=2)
        
        # Quality slider
        quality_frame = tk.Frame(settings_frame)
        quality_frame.pack(fill=tk.X, pady=10)
        
        self.quality_title_label = tk.Label(quality_frame, text="Quality (compression):", font=("Arial", 10))
        self.quality_title_label.pack(anchor=tk.W)
        
        # Quick quality presets
        preset_quality_frame = tk.Frame(quality_frame)
        preset_quality_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(preset_quality_frame, text="Quick presets:", font=("Arial", 9)).pack(side=tk.LEFT, padx=(0, 10))
        
        quality_30_btn = tk.Button(
            preset_quality_frame,
            text="30% (Small)",
            command=lambda: self.set_quality(30),
            bg="#e74c3c",
            fg="white",
            font=("Arial", 9),
            padx=10,
            pady=3,
            cursor="hand2"
        )
        quality_30_btn.pack(side=tk.LEFT, padx=2)
        
        quality_50_btn = tk.Button(
            preset_quality_frame,
            text="50% (Medium)",
            command=lambda: self.set_quality(50),
            bg="#f39c12",
            fg="white",
            font=("Arial", 9),
            padx=10,
            pady=3,
            cursor="hand2"
        )
        quality_50_btn.pack(side=tk.LEFT, padx=2)
        
        quality_85_btn = tk.Button(
            preset_quality_frame,
            text="85% (High)",
            command=lambda: self.set_quality(85),
            bg="#27ae60",
            fg="white",
            font=("Arial", 9),
            padx=10,
            pady=3,
            cursor="hand2"
        )
        quality_85_btn.pack(side=tk.LEFT, padx=2)
        
        # Slider
        slider_frame = tk.Frame(quality_frame)
        slider_frame.pack(fill=tk.X, pady=5)
        
        quality_slider = tk.Scale(
            slider_frame,
            from_=1,
            to=100,
            orient=tk.HORIZONTAL,
            variable=self.quality_var,
            length=300,
            command=self.on_quality_change
        )
        quality_slider.pack(side=tk.LEFT)
        
        self.quality_label = tk.Label(slider_frame, text="50%", font=("Arial", 10, "bold"))
        self.quality_label.pack(side=tk.LEFT, padx=10)
        
        # Output format selection
        format_frame = tk.LabelFrame(parent, text="💾 Output Format", font=("Arial", 11, "bold"), padx=10, pady=10)
        format_frame.pack(fill=tk.X, pady=(0, 15))
        
        format_options_frame = tk.Frame(format_frame)
        format_options_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(format_options_frame, text="Save as:", font=("Arial", 10)).pack(side=tk.LEFT, padx=(0, 10))
        
        formats = [
            ("JPG/JPEG", "jpg"),
            ("PNG", "png"),
            ("WebP", "webp")
        ]
        
        for text, value in formats:
            rb = tk.Radiobutton(
                format_options_frame,
                text=text,
                variable=self.output_format,
                value=value,
                font=("Arial", 10),
                command=self.on_format_change
            )
            rb.pack(side=tk.LEFT, padx=10)
        
        # Format info
        format_info = tk.Label(
            format_frame,
            text="JPG: Lossy, best for photos | PNG: Lossless, supports transparency | WebP: Modern, smaller files",
            font=("Arial", 8, "italic"),
            fg="gray"
        )
        format_info.pack(anchor=tk.W, pady=(5, 0))
        
        # PNG warning
        png_warning = tk.Label(
            format_frame,
            text="⚠️ PNG files can be significantly larger than JPG/WebP (optimized with 256-color palette for web use)",
            font=("Arial", 8, "italic"),
            fg="black",
            wraplength=380,
            justify=tk.LEFT
        )
        png_warning.pack(anchor=tk.W, pady=(3, 0))
        
        # Web presets
        presets_frame = tk.LabelFrame(parent, text="🌐 Web Presets", font=("Arial", 11, "bold"), padx=10, pady=10)
        presets_frame.pack(fill=tk.X, pady=(0, 15))
        
        preset_buttons_frame = tk.Frame(presets_frame)
        preset_buttons_frame.pack()
        
        presets = [
            ("2K (2048x1366)", 2048, 1366),
            ("Full HD (1920x1080)", 1920, 1080),
            ("HD (1280x720)", 1280, 720),
            ("Web (1024x683)", 1024, 683),
            ("Instagram Post (1080x1350)", 1080, 1350),
            ("Instagram Square (1080x1080)", 1080, 1080),
            ("Instagram Story (1080x1920)", 1080, 1920),
            ("Thumbnail (400x300)", 400, 300)
        ]
        
        for i, (name, w, h) in enumerate(presets):
            btn = tk.Button(
                preset_buttons_frame,
                text=name,
                command=lambda w=w, h=h: self.apply_preset(w, h),
                bg="#95a5a6",
                fg="white",
                font=("Arial", 9),
                padx=10,
                pady=5,
                cursor="hand2"
            )
            btn.grid(row=i//2, column=i%2, padx=5, pady=5, sticky=tk.EW)
        
        # Credit text
        credit_text = tk.Label(
            parent,
            text="mediaimmagine s.r.l. - COED Digital Editor IA CUP D97H24001840007\nPR FESR 2021-27 contributo di Regione Friuli-Venezia Giulia",
            font=("Arial", 7),
            fg="black",
            justify=tk.LEFT,
            wraplength=380
        )
        credit_text.pack(anchor=tk.W, pady=(5, 0))
    
    def setup_preview_panel(self, parent):
        """Setup the preview panel"""
        
        # Compact info header (Title + Info on same line)
        header_frame = tk.Frame(parent, bg="#f0f0f0")
        header_frame.pack(fill=tk.X, pady=(0, 5))
        
        # Preview title (left side)
        preview_title = tk.Label(
            header_frame,
            text="📸 Preview",
            font=("Arial", 12, "bold"),
            bg="#f0f0f0"
        )
        preview_title.pack(side=tk.LEFT, padx=(0, 10))
        
        # Preview info label (right side, more compact)
        self.preview_info_label = tk.Label(
            header_frame,
            text="Upload image & click 'Update Preview'",
            font=("Arial", 9),
            bg="#f0f0f0",
            fg="gray",
            anchor=tk.W
        )
        self.preview_info_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Canvas for image preview with scrollbar (adjusted height)
        canvas_frame = tk.Frame(parent, bg="#f0f0f0")
        canvas_frame.pack(fill=tk.BOTH, expand=False, pady=(5, 5))
        
        self.preview_canvas = tk.Canvas(canvas_frame, bg="white", highlightthickness=1, highlightbackground="#ccc", height=552)
        scrollbar_y = tk.Scrollbar(canvas_frame, orient="vertical", command=self.preview_canvas.yview)
        scrollbar_x = tk.Scrollbar(canvas_frame, orient="horizontal", command=self.preview_canvas.xview)
        
        self.preview_canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.preview_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Info section (more compact)
        self.info_frame = tk.LabelFrame(parent, text="ℹ️ Original", font=("Arial", 9, "bold"), padx=8, pady=6, bg="#f0f0f0")
        self.info_frame.pack(fill=tk.X, pady=(8, 5))
        
        self.info_label = tk.Label(self.info_frame, text="Upload an image to see details", fg="gray", justify=tk.LEFT, bg="#f0f0f0", font=("Arial", 8))
        self.info_label.pack(anchor=tk.W)
        
        # Copyright warning label (hidden by default)
        self.copyright_warning_label = tk.Label(
            self.info_frame,
            text="",
            fg="red",
            font=("Arial", 9, "bold"),
            justify=tk.LEFT,
            wraplength=450,
            bg="#f0f0f0"
        )
        self.copyright_warning_label.pack(anchor=tk.W, pady=(3, 0))
        
        # Metadata section (moved here, 2 columns)
        metadata_frame = tk.LabelFrame(parent, text="📝 Metadata (Optional)", font=("Arial", 9, "bold"), padx=8, pady=6, bg="#f0f0f0")
        metadata_frame.pack(fill=tk.X, pady=(8, 5))
        
        # First row: Title and Author
        row1 = tk.Frame(metadata_frame, bg="#f0f0f0")
        row1.pack(fill=tk.X, pady=2)
        
        # Title (left)
        title_frame = tk.Frame(row1, bg="#f0f0f0")
        title_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        tk.Label(title_frame, text="Title:", font=("Arial", 8), bg="#f0f0f0").pack(anchor=tk.W)
        self.metadata_title = tk.Entry(title_frame, font=("Arial", 8))
        self.metadata_title.pack(fill=tk.X)
        
        # Author (right)
        author_frame = tk.Frame(row1, bg="#f0f0f0")
        author_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))
        tk.Label(author_frame, text="Author:", font=("Arial", 8), bg="#f0f0f0").pack(anchor=tk.W)
        self.metadata_author = tk.Entry(author_frame, font=("Arial", 8))
        self.metadata_author.pack(fill=tk.X)
        
        # Second row: Copyright and Description
        row2 = tk.Frame(metadata_frame, bg="#f0f0f0")
        row2.pack(fill=tk.X, pady=2)
        
        # Copyright (left)
        copyright_frame = tk.Frame(row2, bg="#f0f0f0")
        copyright_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        tk.Label(copyright_frame, text="Copyright:", font=("Arial", 8), bg="#f0f0f0").pack(anchor=tk.W)
        self.metadata_copyright = tk.Entry(copyright_frame, font=("Arial", 8))
        self.metadata_copyright.pack(fill=tk.X)
        
        # Description (right)
        description_frame = tk.Frame(row2, bg="#f0f0f0")
        description_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))
        tk.Label(description_frame, text="Description:", font=("Arial", 8), bg="#f0f0f0").pack(anchor=tk.W)
        self.metadata_description = tk.Entry(description_frame, font=("Arial", 8))
        self.metadata_description.pack(fill=tk.X)
        
        # Action buttons (side by side, smaller)
        button_frame = tk.Frame(parent, bg="#f0f0f0")
        button_frame.pack(fill=tk.X, pady=(5, 10))
        
        self.preview_btn = tk.Button(
            button_frame,
            text="🔄 Update Preview",
            command=self.update_preview,
            bg="#f39c12",
            fg="white",
            disabledforeground="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=8,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.preview_btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        self.save_btn = tk.Button(
            button_frame,
            text="💾 Save Image",
            command=self.save_image,
            bg="#27ae60",
            fg="white",
            disabledforeground="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=8,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.save_btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
    def upload_image(self):
        """Upload and load an image"""
        file_path = filedialog.askopenfilename(
            title="Select an image",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.webp"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                self.original_image = Image.open(file_path)
                self.original_path = file_path
                
                # Update file label
                filename = os.path.basename(file_path)
                self.file_label.config(text=f"✓ {filename}", fg="green")
                
                # Update dimensions based on original
                width, height = self.original_image.size
                self.width_var.set(str(width))
                self.height_var.set(str(height))
                
                # Update info with metadata
                file_size = os.path.getsize(file_path) / 1024  # KB
                info_text = f"Original: {width}x{height} px | Size: {file_size:.1f} KB | Format: {self.original_image.format}"
                
                # Extract camera EXIF data if available
                camera_info = self.extract_camera_exif()
                if camera_info:
                    info_text += f"\n{camera_info}"
                
                self.info_label.config(text=info_text, fg="black")
                
                # Check for copyright metadata and show RED warning
                copyright_info = self.extract_copyright_metadata()
                if copyright_info:
                    warning_text = f"WARNING: COPYRIGHT PROTECTED IMAGE\n{copyright_info}"
                    self.copyright_warning_label.config(text=warning_text)
                else:
                    self.copyright_warning_label.config(text="")
                
                # Extract and populate all metadata fields
                self.populate_metadata_fields()
                
                # Enable buttons
                self.preview_btn.config(state=tk.NORMAL)
                self.save_btn.config(state=tk.NORMAL)
                
                # Auto-update preview
                self.update_preview()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image:\n{str(e)}")
    
    def extract_copyright_metadata(self):
        """Extract copyright information from image metadata"""
        if not self.original_image:
            return None
        
        try:
            # Try to get EXIF data
            exif_data = self.original_image.getexif()
            
            if exif_data:
                # EXIF tag 33432 is Copyright
                copyright_tag = 33432
                if copyright_tag in exif_data:
                    return exif_data[copyright_tag]
                
                # Try Artist tag (305)
                artist_tag = 315
                if artist_tag in exif_data:
                    return f"Artist: {exif_data[artist_tag]}"
            
            # Try to get info from image info dict
            if hasattr(self.original_image, 'info'):
                info = self.original_image.info
                
                # Check common metadata keys
                for key in ['copyright', 'Copyright', 'COPYRIGHT', 'author', 'Author', 'creator', 'Creator']:
                    if key in info:
                        return info[key]
            
            return None
            
        except Exception:
            return None
    
    def extract_camera_exif(self):
        """Extract important camera EXIF data"""
        if not self.original_image:
            return None
        
        try:
            exif_data = self.original_image.getexif()
            if not exif_data:
                return None
            
            camera_parts = []
            
            # Camera Make and Model (271, 272)
            make = exif_data.get(271, '').strip()
            model = exif_data.get(272, '').strip()
            if make or model:
                camera = f"{make} {model}".strip()
                camera_parts.append(f"📷 {camera}")
            
            # Aperture (33437 - FNumber)
            if 33437 in exif_data:
                fnumber = exif_data[33437]
                if isinstance(fnumber, tuple):
                    fnumber = fnumber[0] / fnumber[1] if fnumber[1] != 0 else fnumber[0]
                camera_parts.append(f"f/{fnumber:.1f}")
            
            # Shutter Speed (33434 - ExposureTime)
            if 33434 in exif_data:
                exposure = exif_data[33434]
                if isinstance(exposure, tuple):
                    if exposure[0] < exposure[1]:
                        camera_parts.append(f"1/{int(exposure[1]/exposure[0])}s")
                    else:
                        camera_parts.append(f"{exposure[0]/exposure[1]:.2f}s")
                else:
                    camera_parts.append(f"{exposure}s")
            
            # ISO (34855)
            if 34855 in exif_data:
                iso = exif_data[34855]
                if isinstance(iso, tuple):
                    iso = iso[0]
                camera_parts.append(f"ISO {iso}")
            
            # Focal Length (37386)
            if 37386 in exif_data:
                focal = exif_data[37386]
                if isinstance(focal, tuple):
                    focal = focal[0] / focal[1] if focal[1] != 0 else focal[0]
                camera_parts.append(f"{focal:.0f}mm")
            
            if camera_parts:
                return " • ".join(camera_parts)
            
            return None
            
        except Exception:
            return None
    
    def populate_metadata_fields(self):
        """Extract and populate metadata fields from the uploaded image"""
        if not self.original_image:
            return
        
        try:
            # Clear existing fields first
            self.metadata_title.delete(0, tk.END)
            self.metadata_author.delete(0, tk.END)
            self.metadata_copyright.delete(0, tk.END)
            self.metadata_description.delete(0, tk.END)
            
            # Try to get EXIF data (for JPEG/WebP)
            exif_data = self.original_image.getexif()
            
            if exif_data:
                # EXIF tag 270 = ImageDescription
                if 270 in exif_data:
                    description = exif_data[270]
                    # Check if description contains title
                    if ' - ' in description:
                        parts = description.split(' - ', 1)
                        self.metadata_title.insert(0, parts[0])
                        self.metadata_description.insert(0, parts[1])
                    else:
                        self.metadata_description.insert(0, description)
                
                # EXIF tag 315 = Artist
                if 315 in exif_data:
                    self.metadata_author.insert(0, exif_data[315])
                
                # EXIF tag 33432 = Copyright
                if 33432 in exif_data:
                    self.metadata_copyright.insert(0, exif_data[33432])
            
            # Try to get PNG metadata
            if hasattr(self.original_image, 'info'):
                info = self.original_image.info
                
                # Title
                for key in ['Title', 'title']:
                    if key in info and not self.metadata_title.get():
                        self.metadata_title.insert(0, info[key])
                        break
                
                # Author
                for key in ['Author', 'author', 'Artist', 'artist', 'Creator', 'creator']:
                    if key in info and not self.metadata_author.get():
                        self.metadata_author.insert(0, info[key])
                        break
                
                # Copyright
                for key in ['Copyright', 'copyright', 'COPYRIGHT']:
                    if key in info and not self.metadata_copyright.get():
                        self.metadata_copyright.insert(0, info[key])
                        break
                
                # Description
                for key in ['Description', 'description', 'Comment', 'comment']:
                    if key in info and not self.metadata_description.get():
                        self.metadata_description.insert(0, info[key])
                        break
                        
        except Exception as e:
            # If extraction fails, just leave fields empty
            pass
    
    def on_width_change(self, event=None):
        """Handle width change when aspect ratio is locked"""
        if self.keep_aspect_ratio.get() and self.original_image:
            try:
                new_width = int(self.width_var.get())
                orig_width, orig_height = self.original_image.size
                aspect_ratio = orig_height / orig_width
                new_height = int(new_width * aspect_ratio)
                self.height_var.set(str(new_height))
            except ValueError:
                pass
        if self.original_image:
            self.check_crop_needed()
    
    def on_height_change(self, event=None):
        """Handle height change when aspect ratio is locked"""
        if self.keep_aspect_ratio.get() and self.original_image:
            try:
                new_height = int(self.height_var.get())
                orig_width, orig_height = self.original_image.size
                aspect_ratio = orig_width / orig_height
                new_width = int(new_height * aspect_ratio)
                self.width_var.set(str(new_width))
            except ValueError:
                pass
        if self.original_image:
            self.check_crop_needed()
    
    def toggle_aspect_ratio(self):
        """Toggle aspect ratio lock"""
        if self.keep_aspect_ratio.get() and self.original_image:
            # Recalculate height based on current width
            self.on_width_change()
        if self.original_image:
            self.check_crop_needed()
            self.check_blur_applicable()
    
    def toggle_crop_mode(self):
        """Toggle crop mode"""
        if self.original_image:
            # First check if crop is needed
            self.check_crop_needed()
            self.check_blur_applicable()
            
            # Enable/disable manual crop option based on crop mode and need
            if self.crop_mode.get() and self.needs_crop:
                self.manual_crop_check.config(state=tk.NORMAL)
            else:
                self.manual_crop_check.config(state=tk.DISABLED)
                self.manual_crop.set(False)
            
            if self.crop_mode.get():
                self.update_preview()
    
    def toggle_manual_crop(self):
        """Toggle manual crop positioning"""
        if self.manual_crop.get() and self.original_image and self.crop_mode.get():
            # Reset manual offsets
            self.manual_crop_offset_x = 0
            self.manual_crop_offset_y = 0
            # Open interactive crop window
            self.open_interactive_crop()
        else:
            # Close interactive crop window if open
            if self.crop_interactive_window and self.crop_interactive_window.winfo_exists():
                self.crop_interactive_window.destroy()
                self.crop_interactive_window = None
            # Reset to center crop
            self.manual_crop_offset_x = 0
            self.manual_crop_offset_y = 0
            if self.original_image:
                self.update_preview()
    
    def check_crop_needed(self):
        """Check if cropping is needed based on aspect ratios"""
        if not self.original_image or self.keep_aspect_ratio.get():
            self.needs_crop = False
            self.crop_info_label.config(text="")
            self.manual_crop_check.config(state=tk.DISABLED)
            return
        
        try:
            target_width = int(self.width_var.get())
            target_height = int(self.height_var.get())
            orig_width, orig_height = self.original_image.size
            
            orig_ratio = orig_width / orig_height
            target_ratio = target_width / target_height
            
            # Check if aspect ratios are significantly different (more than 1% difference)
            if abs(orig_ratio - target_ratio) > 0.01:
                self.needs_crop = True
                if self.crop_mode.get():
                    # Calculate crop dimensions
                    if orig_ratio > target_ratio:
                        # Original is wider - crop width
                        new_width = int(orig_height * target_ratio)
                        crop_percent = ((orig_width - new_width) / orig_width) * 100
                        position_text = "manual position" if self.manual_crop.get() else "center crop"
                        self.crop_info_label.config(
                            text=f"⚠️ Will crop {crop_percent:.1f}% from sides ({position_text})",
                            fg="orange"
                        )
                    else:
                        # Original is taller - crop height
                        new_height = int(orig_width / target_ratio)
                        crop_percent = ((orig_height - new_height) / orig_height) * 100
                        position_text = "manual position" if self.manual_crop.get() else "center crop"
                        self.crop_info_label.config(
                            text=f"⚠️ Will crop {crop_percent:.1f}% from top/bottom ({position_text})",
                            fg="orange"
                        )
                elif self.blur_background.get():
                    self.crop_info_label.config(
                        text="🌫️ Blur effect enabled - image will be centered with blurred background",
                        fg="blue"
                    )
                else:
                    self.crop_info_label.config(
                        text="ℹ️ Enable 'Crop to fit' to crop image instead of stretching",
                        fg="blue"
                    )
                
            else:
                self.needs_crop = False
                self.crop_info_label.config(text="")
        except (ValueError, ZeroDivisionError):
            self.needs_crop = False
            self.crop_info_label.config(text="")
    
    def update_quality_label(self, value):
        """Update quality percentage label"""
        self.quality_label.config(text=f"{value}%")
    
    def on_quality_change(self, value):
        """Handle quality slider change"""
        self.update_quality_label(value)
        # Auto-update preview if an image is loaded and already has a preview
        if self.original_image and self.resized_image:
            # Use after_idle to avoid too many rapid updates while dragging
            if hasattr(self, '_quality_update_id'):
                self.root.after_cancel(self._quality_update_id)
            self._quality_update_id = self.root.after(300, self.update_preview)
    
    def set_quality(self, quality):
        """Set quality to a specific value"""
        self.quality_var.set(quality)
        self.update_quality_label(quality)
        # Auto-update preview immediately for button clicks
        if self.original_image and self.resized_image:
            self.update_preview()
    
    def apply_preset(self, width, height):
        """Apply a preset dimension"""
        if not self.original_image:
            self.width_var.set(str(width))
            self.height_var.set(str(height))
            return
        
        # Check if aspect ratios differ
        orig_width, orig_height = self.original_image.size
        orig_ratio = orig_width / orig_height
        preset_ratio = width / height
        
        # If aspect ratios differ significantly, automatically enable crop mode
        if abs(orig_ratio - preset_ratio) > 0.01:
            # Uncheck keep aspect ratio
            self.keep_aspect_ratio.set(False)
            # Set dimensions
            self.width_var.set(str(width))
            self.height_var.set(str(height))
            # Enable crop mode
            self.crop_mode.set(True)
            # This will trigger check_crop_needed and enable manual crop
            self.toggle_crop_mode()
        else:
            if self.keep_aspect_ratio.get():
                orig_ratio = orig_width / orig_height
                preset_ratio = width / height
                
                if orig_ratio > preset_ratio:
                    # Wider than preset - fit to width
                    self.width_var.set(str(width))
                    self.on_width_change()
                else:
                    # Taller than preset - fit to height
                    self.height_var.set(str(height))
                    self.on_height_change()
            else:
                self.width_var.set(str(width))
                self.height_var.set(str(height))
                self.check_crop_needed()
    
    def calculate_center_crop_box(self, target_width, target_height):
        """Calculate the crop box for center cropping with optional manual offset"""
        orig_width, orig_height = self.original_image.size
        orig_ratio = orig_width / orig_height
        target_ratio = target_width / target_height
        
        if orig_ratio > target_ratio:
            # Original is wider - crop width
            new_width = int(orig_height * target_ratio)
            center_left = (orig_width - new_width) // 2
            left = center_left + self.manual_crop_offset_x
            # Clamp to valid range
            left = max(0, min(left, orig_width - new_width))
            top = 0
            right = left + new_width
            bottom = orig_height
        else:
            # Original is taller - crop height
            new_height = int(orig_width / target_ratio)
            left = 0
            center_top = (orig_height - new_height) // 2
            top = center_top + self.manual_crop_offset_y
            # Clamp to valid range
            top = max(0, min(top, orig_height - new_height))
            right = orig_width
            bottom = top + new_height
        
        return (left, top, right, bottom)
    
    def create_crop_preview_image(self, crop_box):
        """Create an image showing the crop area with overlay"""
        from PIL import ImageDraw
        
        # Create a copy of the original image
        preview = self.original_image.copy().convert('RGBA')
        
        # Create a semi-transparent overlay
        overlay = Image.new('RGBA', preview.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # Darken areas outside crop box
        left, top, right, bottom = crop_box
        orig_width, orig_height = self.original_image.size
        
        # Draw darkened areas
        if left > 0:
            draw.rectangle([0, 0, left, orig_height], fill=(0, 0, 0, 128))
        if top > 0:
            draw.rectangle([0, 0, orig_width, top], fill=(0, 0, 0, 128))
        if right < orig_width:
            draw.rectangle([right, 0, orig_width, orig_height], fill=(0, 0, 0, 128))
        if bottom < orig_height:
            draw.rectangle([0, bottom, orig_width, orig_height], fill=(0, 0, 0, 128))
        
        # Draw crop box border
        draw.rectangle([left, top, right, bottom], outline=(255, 165, 0, 255), width=3)
        
        # Composite the overlay
        preview = Image.alpha_composite(preview, overlay)
        
        return preview.convert('RGB')
    
    def open_interactive_crop(self):
        """Open interactive crop positioning window"""
        if self.crop_interactive_window and self.crop_interactive_window.winfo_exists():
            self.crop_interactive_window.lift()
            return
        
        # Create new window
        self.crop_interactive_window = tk.Toplevel(self.root)
        self.crop_interactive_window.title("🎯 Position Crop Area")
        self.crop_interactive_window.geometry("900x700")
        
        # Instructions
        instructions = tk.Label(
            self.crop_interactive_window,
            text="Click and drag the orange box to position your crop area.\nThe crop size and ratio are fixed based on your target dimensions.",
            font=("Arial", 11),
            bg="#f0f0f0",
            pady=10
        )
        instructions.pack(fill=tk.X)
        
        # Create canvas for interactive preview
        canvas_frame = tk.Frame(self.crop_interactive_window)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.crop_canvas = tk.Canvas(canvas_frame, bg="gray", cursor="cross")
        scrollbar_y = tk.Scrollbar(canvas_frame, orient="vertical", command=self.crop_canvas.yview)
        scrollbar_x = tk.Scrollbar(canvas_frame, orient="horizontal", command=self.crop_canvas.xview)
        
        self.crop_canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.crop_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Calculate crop box
        try:
            target_width = int(self.width_var.get())
            target_height = int(self.height_var.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid dimensions")
            self.crop_interactive_window.destroy()
            return
        
        # Give the window time to render
        self.crop_interactive_window.update_idletasks()
        
        # Display the image with crop overlay
        self.update_interactive_crop_display()
        
        # Bind mouse events for dragging
        self.crop_canvas.bind("<ButtonPress-1>", self.on_crop_drag_start)
        self.crop_canvas.bind("<B1-Motion>", self.on_crop_drag_motion)
        self.crop_canvas.bind("<ButtonRelease-1>", self.on_crop_drag_end)
        
        # Buttons
        button_frame = tk.Frame(self.crop_interactive_window)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        reset_btn = tk.Button(
            button_frame,
            text="↺ Reset to Center",
            command=self.reset_crop_position,
            bg="#95a5a6",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=8
        )
        reset_btn.pack(side=tk.LEFT, padx=5)
        
        apply_btn = tk.Button(
            button_frame,
            text="✓ Apply & Close",
            command=self.apply_and_close_crop,
            bg="#27ae60",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=8
        )
        apply_btn.pack(side=tk.RIGHT, padx=5)
    
    def update_interactive_crop_display(self):
        """Update the interactive crop canvas display"""
        if not hasattr(self, 'crop_canvas') or not self.crop_canvas or not self.crop_canvas.winfo_exists():
            return
        
        # Ensure canvas has been rendered
        self.crop_canvas.update_idletasks()
        
        # Clear canvas
        self.crop_canvas.delete("all")
        
        # Calculate current crop box
        try:
            target_width = int(self.width_var.get())
            target_height = int(self.height_var.get())
            crop_box = self.calculate_center_crop_box(target_width, target_height)
        except (ValueError, Exception):
            return
        
        # Scale image to fit canvas (max 800x600)
        display_img = self.original_image.copy()
        max_size = (800, 600)
        display_img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Calculate scale factor
        orig_width, orig_height = self.original_image.size
        display_width, display_height = display_img.size
        scale_x = display_width / orig_width
        scale_y = display_height / orig_height
        
        # Store scale for mouse calculations
        self.crop_scale_x = scale_x
        self.crop_scale_y = scale_y
        
        # Display image - MUST keep reference to prevent garbage collection
        self.crop_display_photo = ImageTk.PhotoImage(display_img)
        self.crop_image_id = self.crop_canvas.create_image(0, 0, anchor="nw", image=self.crop_display_photo)
        
        # Force canvas update
        self.crop_canvas.update()
        
        # Draw crop box (scaled)
        left, top, right, bottom = crop_box
        scaled_left = left * scale_x
        scaled_top = top * scale_y
        scaled_right = right * scale_x
        scaled_bottom = bottom * scale_y
        
        # Draw darkened areas outside crop
        # Top
        if scaled_top > 0:
            self.crop_canvas.create_rectangle(
                0, 0, display_width, scaled_top,
                fill="black", stipple="gray50", outline=""
            )
        # Bottom
        if scaled_bottom < display_height:
            self.crop_canvas.create_rectangle(
                0, scaled_bottom, display_width, display_height,
                fill="black", stipple="gray50", outline=""
            )
        # Left
        if scaled_left > 0:
            self.crop_canvas.create_rectangle(
                0, scaled_top, scaled_left, scaled_bottom,
                fill="black", stipple="gray50", outline=""
            )
        # Right
        if scaled_right < display_width:
            self.crop_canvas.create_rectangle(
                scaled_right, scaled_top, display_width, scaled_bottom,
                fill="black", stipple="gray50", outline=""
            )
        
        # Draw crop box border
        self.crop_canvas.create_rectangle(
            scaled_left, scaled_top, scaled_right, scaled_bottom,
            outline="orange", width=3, tags="cropbox"
        )
        
        # Add center crosshair in crop box
        center_x = (scaled_left + scaled_right) / 2
        center_y = (scaled_top + scaled_bottom) / 2
        crosshair_size = 20
        self.crop_canvas.create_line(
            center_x - crosshair_size, center_y,
            center_x + crosshair_size, center_y,
            fill="orange", width=2, tags="cropbox"
        )
        self.crop_canvas.create_line(
            center_x, center_y - crosshair_size,
            center_x, center_y + crosshair_size,
            fill="orange", width=2, tags="cropbox"
        )
        
        # Configure scroll region
        self.crop_canvas.configure(scrollregion=(0, 0, display_width, display_height))
        
        # Final update
        self.crop_canvas.update_idletasks()
    
    def on_crop_drag_start(self, event):
        """Handle start of crop box drag"""
        self.dragging = True
        self.drag_start_x = event.x
        self.drag_start_y = event.y
    
    def on_crop_drag_motion(self, event):
        """Handle crop box dragging"""
        if not self.dragging:
            return
        
        # Calculate offset in display coordinates
        dx = event.x - self.drag_start_x
        dy = event.y - self.drag_start_y
        
        # Convert to original image coordinates
        orig_dx = int(dx / self.crop_scale_x)
        orig_dy = int(dy / self.crop_scale_y)
        
        # Update offsets
        self.manual_crop_offset_x += orig_dx
        self.manual_crop_offset_y += orig_dy
        
        # Update display
        self.update_interactive_crop_display()
        
        # Reset drag start for next motion
        self.drag_start_x = event.x
        self.drag_start_y = event.y
    
    def on_crop_drag_end(self, event):
        """Handle end of crop box drag"""
        self.dragging = False
        # Update main preview
        self.update_preview()
    
    def reset_crop_position(self):
        """Reset crop to center position"""
        self.manual_crop_offset_x = 0
        self.manual_crop_offset_y = 0
        self.update_interactive_crop_display()
        self.update_preview()
    
    def apply_and_close_crop(self):
        """Apply crop position and close interactive window"""
        if self.crop_interactive_window:
            self.crop_interactive_window.destroy()
            self.crop_interactive_window = None
        self.update_preview()
    
    def check_blur_applicable(self):
        """Check if blur effect is applicable and enable/disable the option"""
        if not self.original_image:
            self.blur_background_check.config(state=tk.DISABLED)
            self.blur_background.set(False)
            self.blur_strength_frame.pack_forget()
            return
        
        try:
            target_width = int(self.width_var.get())
            target_height = int(self.height_var.get())
            orig_width, orig_height = self.original_image.size
            
            orig_ratio = orig_width / orig_height
            target_ratio = target_width / target_height
            
            # Blur is only applicable when:
            # 1. Aspect ratios differ significantly
            # 2. NOT in crop mode
            # 3. Converting portrait to landscape (orig_ratio < target_ratio)
            if (abs(orig_ratio - target_ratio) > 0.01 and 
                not self.crop_mode.get() and 
                orig_ratio < target_ratio):
                self.blur_background_check.config(state=tk.NORMAL)
            else:
                self.blur_background_check.config(state=tk.DISABLED)
                self.blur_background.set(False)
                self.blur_strength_frame.pack_forget()
                
        except (ValueError, ZeroDivisionError):
            self.blur_background_check.config(state=tk.DISABLED)
            self.blur_background.set(False)
            self.blur_strength_frame.pack_forget()
    
    def toggle_blur_background(self):
        """Toggle blur background effect"""
        if self.blur_background.get():
            # Show blur strength slider
            self.blur_strength_frame.pack(anchor=tk.W, pady=(0, 5))
        else:
            # Hide blur strength slider
            self.blur_strength_frame.pack_forget()
        
        # Update preview if image is loaded
        if self.original_image:
            self.check_crop_needed()
            self.update_preview()
    
    def on_blur_strength_change(self, value):
        """Handle blur strength slider change"""
        self.blur_strength_label.config(text=str(value))
        # Auto-update preview if an image is loaded and already has a preview
        if self.original_image and self.resized_image and self.blur_background.get():
            # Use after_idle to avoid too many rapid updates while dragging
            if hasattr(self, '_blur_update_id'):
                self.root.after_cancel(self._blur_update_id)
            self._blur_update_id = self.root.after(300, self.update_preview)
    
    def on_format_change(self):
        """Handle output format change - update preview to recalculate file size"""
        if self.original_image and self.resized_image:
            self.update_preview()
    
    def create_blur_background_image(self, target_width, target_height):
        """Create an image with blurred background and centered original"""
        # Create blurred background
        background = self.original_image.copy()
        
        # Resize background to fill the target dimensions
        background.thumbnail((target_width, target_height), Image.Resampling.LANCZOS)
        
        # Create a new image with target dimensions
        bg_img = Image.new('RGB', (target_width, target_height), (0, 0, 0))
        
        # Paste and stretch the background
        background_resized = self.original_image.resize((target_width, target_height), Image.Resampling.LANCZOS)
        
        # Apply blur with user-defined strength
        blur_radius = self.blur_strength.get()
        background_blurred = background_resized.filter(ImageFilter.GaussianBlur(radius=blur_radius))
        
        # Use blurred background
        bg_img = background_blurred
        
        # Calculate size for centered original image (maintain aspect ratio)
        orig_width, orig_height = self.original_image.size
        orig_ratio = orig_width / orig_height
        
        # Fit the original image to the height (since it's portrait)
        new_height = target_height
        new_width = int(new_height * orig_ratio)
        
        # If width exceeds target, fit to width instead
        if new_width > target_width:
            new_width = target_width
            new_height = int(new_width / orig_ratio)
        
        # Resize original image
        centered_img = self.original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Calculate position to center the image
        x_offset = (target_width - new_width) // 2
        y_offset = (target_height - new_height) // 2
        
        # Paste centered image on blurred background
        if centered_img.mode == 'RGBA':
            bg_img.paste(centered_img, (x_offset, y_offset), centered_img)
        else:
            bg_img.paste(centered_img, (x_offset, y_offset))
        
        return bg_img
    
    def update_preview(self):
        """Update the preview with resized image"""
        if not self.original_image:
            messagebox.showwarning("No Image", "Please upload an image first")
            return
        
        try:
            new_width = int(self.width_var.get())
            new_height = int(self.height_var.get())
            
            if new_width <= 0 or new_height <= 0:
                messagebox.showerror("Invalid Dimensions", "Width and height must be positive numbers")
                return
            
            # Check if we need to crop
            self.check_crop_needed()
            self.check_blur_applicable()
            
            # Create resized image
            if self.crop_mode.get() and self.needs_crop:
                # Crop first, then resize
                crop_box = self.calculate_center_crop_box(new_width, new_height)
                self.crop_box = crop_box
                cropped = self.original_image.crop(crop_box)
                self.resized_image = cropped.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Create crop preview visualization
                self.crop_preview_image = self.create_crop_preview_image(crop_box)
            elif self.blur_background.get() and self.needs_crop:
                # Apply blur background effect
                self.resized_image = self.create_blur_background_image(new_width, new_height)
                self.crop_preview_image = None
            else:
                # Regular resize (will stretch if aspect ratios don't match)
                self.resized_image = self.original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                self.crop_preview_image = None
            
            # Calculate estimated file size based on selected format
            import io
            temp_buffer = io.BytesIO()
            temp_img = self.resized_image.copy()
            
            # Get selected format
            selected_format = self.output_format.get().upper()
            if selected_format == 'JPG':
                selected_format = 'JPEG'
            
            # Prepare save parameters based on format
            save_kwargs = {}
            
            if selected_format == 'JPEG':
                # Convert RGBA to RGB for JPEG
                if temp_img.mode == 'RGBA':
                    background = Image.new('RGB', temp_img.size, (255, 255, 255))
                    background.paste(temp_img, mask=temp_img.split()[3] if len(temp_img.split()) == 4 else None)
                    temp_img = background
                save_kwargs = {'quality': self.quality_var.get(), 'optimize': True}
                
            elif selected_format == 'PNG':
                # PNG: Always use maximum compression for smallest file size
                # Convert to palette mode if possible to reduce size dramatically
                if temp_img.mode == 'RGBA':
                    # Keep RGBA for transparency
                    save_kwargs = {'optimize': True, 'compress_level': 9}
                elif temp_img.mode == 'RGB':
                    # Try to convert to palette mode for smaller files
                    try:
                        # Convert to P mode (palette) with adaptive palette for smaller files
                        temp_img = temp_img.convert('P', palette=Image.ADAPTIVE, colors=256)
                        save_kwargs = {'optimize': True, 'compress_level': 9}
                    except:
                        save_kwargs = {'optimize': True, 'compress_level': 9}
                else:
                    save_kwargs = {'optimize': True, 'compress_level': 9}
                
            elif selected_format == 'WEBP':
                save_kwargs = {'quality': self.quality_var.get(), 'method': 6}
            
            temp_img.save(temp_buffer, format=selected_format, **save_kwargs)
            estimated_size_kb = len(temp_buffer.getvalue()) / 1024
            temp_buffer.close()
            
            # Update info label - compact horizontal format
            crop_text = ""
            if self.crop_mode.get() and self.needs_crop and self.crop_box:
                left, top, right, bottom = self.crop_box
                crop_text = f" ✂️ From:{right-left}x{bottom-top}"
            
            # Determine file size color based on thresholds
            if estimated_size_kb > 130:
                size_color = "red"
                size_warning = "⚠️"
            elif estimated_size_kb > 90:
                size_color = "orange"
                size_warning = "⚠️"
            else:
                size_color = "green"
                size_warning = "✓"
            
            # Compact single line format
            info_text = f"📐 {new_width}x{new_height}px  •  🎚️ Q:{self.quality_var.get()}%{crop_text}"
            self.preview_info_label.config(text=info_text, fg="black")
            
            # Create separate label for file size with color coding
            if not hasattr(self, 'size_warning_label'):
                self.size_warning_label = tk.Label(
                    self.preview_info_label.master,
                    font=("Arial", 9, "bold"),
                    bg="#f0f0f0"
                )
                # Pack it on the same line (right side)
                self.size_warning_label.pack(side=tk.RIGHT, padx=(5, 0))
            
            size_text = f"📊 {estimated_size_kb:.1f}KB {size_warning}"
            self.size_warning_label.config(text=size_text, fg=size_color)
            
            # Clear previous preview by deleting all canvas items
            self.preview_canvas.delete("all")
            
            # If cropping, show crop visualization and final result side by side
            if self.crop_mode.get() and self.needs_crop and self.crop_preview_image:
                # Create a frame to hold both previews horizontally
                preview_frame = tk.Frame(self.preview_canvas, bg="white")
                
                # Left side - Crop visualization
                left_frame = tk.Frame(preview_frame, bg="white")
                left_frame.pack(side=tk.LEFT, padx=10)
                
                tk.Label(
                    left_frame,
                    text="📍 Crop Area",
                    font=("Arial", 10, "bold"),
                    bg="white"
                ).pack(pady=5)
                
                max_preview_size = (300, 400)
                crop_display = self.crop_preview_image.copy()
                crop_display.thumbnail(max_preview_size, Image.Resampling.LANCZOS)
                
                crop_photo = ImageTk.PhotoImage(crop_display)
                crop_label = tk.Label(left_frame, image=crop_photo, bg="white", bd=1, relief=tk.SOLID)
                crop_label.image = crop_photo
                crop_label.pack(pady=5)
                
                # Separator
                separator_frame = tk.Frame(preview_frame, bg="white")
                separator_frame.pack(side=tk.LEFT, padx=5)
                tk.Label(separator_frame, text="→", font=("Arial", 20), bg="white").pack(pady=200)
                
                # Right side - Final result
                right_frame = tk.Frame(preview_frame, bg="white")
                right_frame.pack(side=tk.LEFT, padx=10)
                
                tk.Label(
                    right_frame,
                    text="✅ Final Result",
                    font=("Arial", 10, "bold"),
                    bg="white"
                ).pack(pady=5)
                
                result_display = self.resized_image.copy()
                result_display.thumbnail(max_preview_size, Image.Resampling.LANCZOS)
                
                result_photo = ImageTk.PhotoImage(result_display)
                result_label = tk.Label(right_frame, image=result_photo, bg="white", bd=1, relief=tk.SOLID)
                result_label.image = result_photo
                result_label.pack(pady=5)
                
                self.preview_canvas_window = self.preview_canvas.create_window(10, 10, anchor="nw", window=preview_frame)
            else:
                # Regular preview (no crop) - recreate the preview image label
                preview_frame = tk.Frame(self.preview_canvas, bg="white")
                
                max_preview_size = (500, 500)
                display_img = self.resized_image.copy()
                display_img.thumbnail(max_preview_size, Image.Resampling.LANCZOS)
                
                photo = ImageTk.PhotoImage(display_img)
                img_label = tk.Label(preview_frame, image=photo, bg="white")
                img_label.image = photo  # Keep reference
                img_label.pack(pady=10)
                
                self.preview_canvas_window = self.preview_canvas.create_window(10, 10, anchor="nw", window=preview_frame)
            
            # Update canvas scroll region
            self.preview_canvas.update_idletasks()
            self.preview_canvas.configure(scrollregion=self.preview_canvas.bbox("all"))
            
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for width and height")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to preview image:\n{str(e)}")
    
    def save_image(self):
        """Save the resized image"""
        if not self.original_image:
            messagebox.showwarning("No Image", "Please upload an image first")
            return
        
        try:
            new_width = int(self.width_var.get())
            new_height = int(self.height_var.get())
            
            if new_width <= 0 or new_height <= 0:
                messagebox.showerror("Invalid Dimensions", "Width and height must be positive numbers")
                return
            
            # Get save location with trieste@news_ prefix and selected format
            original_name = Path(self.original_path).stem
            
            # Get extension based on selected format
            format_extensions = {
                'jpg': '.jpg',
                'png': '.png',
                'webp': '.webp'
            }
            selected_ext = format_extensions.get(self.output_format.get(), '.jpg')
            
            default_name = f"trieste@news_{original_name}{selected_ext}"
            
            # Set filetypes based on selected format
            if self.output_format.get() == 'jpg':
                filetypes = [("JPEG", "*.jpg *.jpeg"), ("All files", "*.*")]
                defaultextension = '.jpg'
            elif self.output_format.get() == 'png':
                filetypes = [("PNG", "*.png"), ("All files", "*.*")]
                defaultextension = '.png'
            else:  # webp
                filetypes = [("WebP", "*.webp"), ("All files", "*.*")]
                defaultextension = '.webp'
            
            save_path = filedialog.asksaveasfilename(
                defaultextension=defaultextension,
                initialfile=default_name,
                filetypes=filetypes
            )
            
            if save_path:
                # Use the previewed resized image if available, otherwise create new one
                if self.resized_image:
                    resized = self.resized_image
                else:
                    resized = self.original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Determine save parameters based on format
                save_kwargs = {}
                
                if save_path.lower().endswith(('.jpg', '.jpeg')):
                    save_kwargs = {
                        'quality': self.quality_var.get(),
                        'optimize': True
                    }
                    # Convert RGBA to RGB if necessary
                    if resized.mode == 'RGBA':
                        # Create white background
                        background = Image.new('RGB', resized.size, (255, 255, 255))
                        background.paste(resized, mask=resized.split()[3] if len(resized.split()) == 4 else None)
                        resized = background
                
                elif save_path.lower().endswith('.webp'):
                    save_kwargs = {
                        'quality': self.quality_var.get(),
                        'method': 6  # Better compression
                    }
                
                elif save_path.lower().endswith('.png'):
                    # PNG uses compression level (0-9) not quality
                    # Quality slider translates to compression:
                    # High quality (80-100) = low compression (0-3)
                    # Medium quality (50-79) = medium compression (4-6)
                    # Low quality (1-49) = high compression (7-9)
                    quality = self.quality_var.get()
                    if quality >= 80:
                        compress_level = 3
                    elif quality >= 50:
                        compress_level = 6
                    else:
                        compress_level = 9
                    
                    save_kwargs = {
                        'optimize': True,
                        'compress_level': compress_level
                    }
                
                # Add metadata if provided
                metadata_info = {}
                
                if self.metadata_title.get().strip():
                    metadata_info['Title'] = self.metadata_title.get().strip()
                if self.metadata_author.get().strip():
                    metadata_info['Author'] = self.metadata_author.get().strip()
                if self.metadata_copyright.get().strip():
                    metadata_info['Copyright'] = self.metadata_copyright.get().strip()
                if self.metadata_description.get().strip():
                    metadata_info['Description'] = self.metadata_description.get().strip()
                
                # For PNG, add metadata to info dict
                if save_path.lower().endswith('.png') and metadata_info:
                    pnginfo = None
                    try:
                        from PIL import PngImagePlugin
                        pnginfo = PngImagePlugin.PngInfo()
                        for key, value in metadata_info.items():
                            pnginfo.add_text(key, value)
                        save_kwargs['pnginfo'] = pnginfo
                    except:
                        pass
                
                # For JPEG/WebP, try to add EXIF metadata
                if (save_path.lower().endswith(('.jpg', '.jpeg', '.webp')) and metadata_info):
                    try:
                        # Get existing exif or create new
                        exif = resized.getexif()
                        
                        # EXIF tags for metadata
                        # 270 = ImageDescription
                        # 315 = Artist
                        # 33432 = Copyright
                        
                        if 'Description' in metadata_info:
                            exif[270] = metadata_info['Description']
                        if 'Author' in metadata_info:
                            exif[315] = metadata_info['Author']
                        if 'Copyright' in metadata_info:
                            exif[33432] = metadata_info['Copyright']
                        if 'Title' in metadata_info:
                            exif[270] = metadata_info.get('Title', '') + ' - ' + metadata_info.get('Description', '')
                        
                        save_kwargs['exif'] = exif
                    except:
                        pass
                
                # Save the image
                resized.save(save_path, **save_kwargs)
                
                # Show success with file info
                file_size = os.path.getsize(save_path) / 1024
                messagebox.showinfo(
                    "Success",
                    f"Image saved successfully!\n\n"
                    f"Location: {save_path}\n"
                    f"Dimensions: {new_width}x{new_height} px\n"
                    f"File size: {file_size:.1f} KB"
                )
                
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for width and height")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save image:\n{str(e)}")


def main():
    root = tk.Tk()
    app = ImageResizerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

