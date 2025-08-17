#!/usr/bin/env python3

import os
import sys
import json
from pathlib import Path
from typing import Optional, List
import tkinter as tk
from tkinter import messagebox, filedialog
import customtkinter as ctk
from PIL import Image, ImageGrab, ImageTk
import pyperclip


class SettingsWindow:
    def __init__(self, parent, current_settings):
        self.parent = parent
        self.settings = current_settings.copy()
        
        # Create window
        self.window = ctk.CTkToplevel(parent.root)
        self.window.title("Settings")
        self.window.geometry("500x300")
        self.window.transient(parent.root)
        self.window.grab_set()
        
        self.setup_ui()
        self.window.focus()
        
    def setup_ui(self):
        """Setup settings UI"""
        main_frame = ctk.CTkFrame(self.window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Save directory setting
        dir_label = ctk.CTkLabel(main_frame, text="Save Directory:", font=ctk.CTkFont(size=14))
        dir_label.grid(row=0, column=0, sticky="w", pady=(0, 10))
        
        dir_frame = ctk.CTkFrame(main_frame)
        dir_frame.grid(row=0, column=1, sticky="ew", pady=(0, 10), padx=(10, 0))
        
        self.dir_entry = ctk.CTkEntry(dir_frame, width=250)
        self.dir_entry.pack(side="left", padx=(0, 10))
        self.dir_entry.insert(0, self.settings['save_directory'])
        
        browse_btn = ctk.CTkButton(dir_frame, text="Browse", width=70, command=self.browse_directory)
        browse_btn.pack(side="right")
        
        # Max images setting
        max_label = ctk.CTkLabel(main_frame, text="Max Images:", font=ctk.CTkFont(size=14))
        max_label.grid(row=1, column=0, sticky="w", pady=(10, 10))
        
        max_frame = ctk.CTkFrame(main_frame)
        max_frame.grid(row=1, column=1, sticky="w", pady=(10, 10), padx=(10, 0))
        
        self.max_slider = ctk.CTkSlider(max_frame, from_=5, to=50, number_of_steps=45, width=200)
        self.max_slider.pack(side="left", padx=(0, 10))
        self.max_slider.set(self.settings['max_images'])
        self.max_slider.configure(command=self.update_max_label)
        
        self.max_value_label = ctk.CTkLabel(max_frame, text=str(int(self.settings['max_images'])))
        self.max_value_label.pack(side="left")
        
        # Theme setting
        theme_label = ctk.CTkLabel(main_frame, text="Theme:", font=ctk.CTkFont(size=14))
        theme_label.grid(row=2, column=0, sticky="w", pady=(10, 10))
        
        self.theme_var = ctk.StringVar(value=self.settings['theme'])
        theme_menu = ctk.CTkOptionMenu(main_frame, values=["dark", "light"], variable=self.theme_var, width=150)
        theme_menu.grid(row=2, column=1, sticky="w", pady=(10, 10), padx=(10, 0))
        
        # Thumbnail size setting
        thumb_label = ctk.CTkLabel(main_frame, text="Thumbnail Size:", font=ctk.CTkFont(size=14))
        thumb_label.grid(row=3, column=0, sticky="w", pady=(10, 10))
        
        thumb_frame = ctk.CTkFrame(main_frame)
        thumb_frame.grid(row=3, column=1, sticky="w", pady=(10, 10), padx=(10, 0))
        
        self.thumb_slider = ctk.CTkSlider(thumb_frame, from_=50, to=200, number_of_steps=15, width=200)
        self.thumb_slider.pack(side="left", padx=(0, 10))
        self.thumb_slider.set(self.settings.get('thumbnail_size', 100))
        self.thumb_slider.configure(command=self.update_thumb_label)
        
        self.thumb_value_label = ctk.CTkLabel(thumb_frame, text=f"{int(self.settings.get('thumbnail_size', 100))}px")
        self.thumb_value_label.pack(side="left")
        
        # Configure grid weights
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Buttons
        button_frame = ctk.CTkFrame(self.window)
        button_frame.pack(fill="x", pady=(0, 20), padx=20)
        
        save_btn = ctk.CTkButton(button_frame, text="Save", command=self.save_settings)
        save_btn.pack(side="right", padx=(10, 0))
        
        cancel_btn = ctk.CTkButton(button_frame, text="Cancel", command=self.window.destroy)
        cancel_btn.pack(side="right")
        
    def browse_directory(self):
        """Browse for directory"""
        directory = filedialog.askdirectory(initialdir=self.dir_entry.get())
        if directory:
            self.dir_entry.delete(0, 'end')
            self.dir_entry.insert(0, directory)
    
    def update_max_label(self, value):
        """Update max images label"""
        self.max_value_label.configure(text=str(int(value)))
    
    def update_thumb_label(self, value):
        """Update thumbnail size label"""
        self.thumb_value_label.configure(text=f"{int(value)}px")
    
    def save_settings(self):
        """Save settings and close"""
        self.settings['save_directory'] = self.dir_entry.get()
        self.settings['max_images'] = int(self.max_slider.get())
        self.settings['theme'] = self.theme_var.get()
        self.settings['thumbnail_size'] = int(self.thumb_slider.get())
        
        # Apply settings to parent
        self.parent.apply_settings(self.settings)
        self.window.destroy()


class ImagePathifier:
    def __init__(self):
        self.settings = self.load_settings()
        self.save_dir = Path(self.settings['save_directory'])
        self.save_dir.mkdir(exist_ok=True, parents=True)
        
        # Image management
        self.image_files = []
        self.thumbnails = {}
        self.load_existing_images()
        
        # Setup window
        self.root = ctk.CTk()
        self.root.title("Image Pathifier")
        
        # Set theme
        ctk.set_appearance_mode(self.settings['theme'])
        ctk.set_default_color_theme("blue")
        
        # Window configuration
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        self.setup_ui()
        self.bind_shortcuts()
        self.update_thumbnail_grid()
    
    def load_settings(self):
        """Load settings from JSON file"""
        settings_file = Path('settings.json')
        default_settings = {
            'save_directory': './saved_images',
            'max_images': 20,
            'theme': 'dark',
            'thumbnail_size': 100
        }
        
        if settings_file.exists():
            try:
                with open(settings_file, 'r') as f:
                    loaded = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    default_settings.update(loaded)
            except:
                pass
        
        return default_settings
    
    def save_settings(self):
        """Save settings to JSON file"""
        with open('settings.json', 'w') as f:
            json.dump(self.settings, f, indent=2)
    
    def apply_settings(self, new_settings):
        """Apply new settings"""
        theme_changed = self.settings['theme'] != new_settings['theme']
        dir_changed = self.settings['save_directory'] != new_settings['save_directory']
        
        self.settings = new_settings
        self.save_settings()
        
        if theme_changed:
            ctk.set_appearance_mode(self.settings['theme'])
            
        if dir_changed:
            self.save_dir = Path(self.settings['save_directory'])
            self.save_dir.mkdir(exist_ok=True, parents=True)
            self.load_existing_images()
            self.update_thumbnail_grid()
        
        # Clean up old images if max_images reduced
        self.cleanup_old_images()
        self.update_thumbnail_grid()
    
    def load_existing_images(self):
        """Load existing images from save directory"""
        self.image_files = []
        if self.save_dir.exists():
            # Look for numbered images
            for i in range(1, self.settings['max_images'] + 1):
                img_path = self.save_dir / f"img_{i:04d}.png"
                if img_path.exists():
                    self.image_files.append(img_path)
    
    def get_next_filename(self):
        """Get next sequential filename"""
        # Find the highest number
        max_num = 0
        for img_path in self.image_files:
            try:
                num = int(img_path.stem.split('_')[1])
                max_num = max(max_num, num)
            except:
                pass
        
        # Next number
        next_num = max_num + 1
        
        # If we exceed max_images, wrap around to 1
        if next_num > self.settings['max_images']:
            next_num = 1
            
        return f"img_{next_num:04d}.png"
    
    def cleanup_old_images(self):
        """Remove images exceeding max_images limit"""
        while len(self.image_files) > self.settings['max_images']:
            # Remove oldest (first in list)
            old_file = self.image_files.pop(0)
            try:
                old_file.unlink()
            except:
                pass
    
    def setup_ui(self):
        """Setup the user interface"""
        # Menu bar frame
        menu_frame = ctk.CTkFrame(self.root, height=40)
        menu_frame.pack(fill="x", padx=5, pady=5)
        
        # Title
        title_label = ctk.CTkLabel(
            menu_frame, 
            text="Image Pathifier", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(side="left", padx=10)
        
        # Settings button
        settings_btn = ctk.CTkButton(
            menu_frame,
            text="⚙ Settings",
            width=100,
            command=self.open_settings
        )
        settings_btn.pack(side="right", padx=10)
        
        # Instructions
        instruction_frame = ctk.CTkFrame(self.root)
        instruction_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        instruction_label = ctk.CTkLabel(
            instruction_frame,
            text="Press Ctrl+V to paste an image from clipboard → Path will be copied automatically",
            font=ctk.CTkFont(size=12)
        )
        instruction_label.pack(pady=5)
        
        # Status
        self.status_label = ctk.CTkLabel(
            instruction_frame,
            text=f"Images: {len(self.image_files)}/{self.settings['max_images']} | Save to: {self.save_dir}",
            font=ctk.CTkFont(size=10)
        )
        self.status_label.pack(pady=(0, 5))
        
        # Thumbnail grid
        self.grid_frame = ctk.CTkScrollableFrame(self.root)
        self.grid_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Configure grid columns
        for i in range(6):  # 6 columns
            self.grid_frame.grid_columnconfigure(i, weight=1)
    
    def bind_shortcuts(self):
        """Bind keyboard shortcuts"""
        self.root.bind('<Control-v>', lambda e: self.paste_image())
    
    def paste_image(self):
        """Handle paste action - save image and copy path"""
        try:
            img = ImageGrab.grabclipboard()
            if isinstance(img, Image.Image):
                # Get next filename
                filename = self.get_next_filename()
                filepath = self.save_dir / filename
                
                # Check if file exists and should be overwritten
                if filepath.exists():
                    # Remove from list
                    if filepath in self.image_files:
                        self.image_files.remove(filepath)
                
                # Save image
                img.save(filepath, 'PNG')
                
                # Add to list
                self.image_files.append(filepath)
                
                # Clean up old images
                self.cleanup_old_images()
                
                # Copy path to clipboard
                pyperclip.copy(str(filepath.absolute()))
                
                # Update UI
                self.update_thumbnail_grid()
                self.update_status(f"Saved {filename} - Path copied to clipboard!")
                
            else:
                self.update_status("No image in clipboard")
                messagebox.showwarning("No Image", "No image found in clipboard")
                
        except Exception as e:
            self.update_status(f"Error: {e}")
            messagebox.showerror("Error", f"Failed to process image: {e}")
    
    def update_thumbnail_grid(self):
        """Update thumbnail grid display"""
        # Clear existing thumbnails
        for widget in self.grid_frame.winfo_children():
            widget.destroy()
        self.thumbnails.clear()
        
        # Sort images by number
        self.image_files.sort(key=lambda p: int(p.stem.split('_')[1]) if p.stem.startswith('img_') else 0)
        
        # Create thumbnails
        thumb_size = self.settings.get('thumbnail_size', 100)
        columns = 6
        
        for idx, img_path in enumerate(self.image_files):
            if not img_path.exists():
                continue
                
            row = idx // columns
            col = idx % columns
            
            # Create frame for thumbnail
            thumb_frame = ctk.CTkFrame(self.grid_frame)
            thumb_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            
            try:
                # Load and resize image
                img = Image.open(img_path)
                img.thumbnail((thumb_size, thumb_size), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                
                # Create label with image
                img_label = tk.Label(thumb_frame, image=photo, bg=thumb_frame.cget("fg_color")[0])
                img_label.image = photo  # Keep reference
                img_label.pack(padx=2, pady=2)
                
                # Bind click event
                img_label.bind("<Button-1>", lambda e, path=img_path: self.copy_image_path(path))
                
                # Add filename label
                name_label = ctk.CTkLabel(
                    thumb_frame, 
                    text=img_path.name, 
                    font=ctk.CTkFont(size=10)
                )
                name_label.pack()
                
                # Add tooltip on hover
                img_label.bind("<Enter>", lambda e, path=img_path: self.update_status(f"Click to copy: {path}"))
                img_label.bind("<Leave>", lambda e: self.update_status(f"Images: {len(self.image_files)}/{self.settings['max_images']}"))
                
            except Exception as e:
                print(f"Error loading thumbnail for {img_path}: {e}")
        
        self.update_status(f"Images: {len(self.image_files)}/{self.settings['max_images']}")
    
    def copy_image_path(self, img_path):
        """Copy image path to clipboard"""
        path_str = str(img_path.absolute())
        pyperclip.copy(path_str)
        self.update_status(f"Copied: {path_str}")
    
    def update_status(self, message: str):
        """Update status message"""
        self.status_label.configure(text=message)
    
    def open_settings(self):
        """Open settings window"""
        SettingsWindow(self, self.settings)
    
    def run(self):
        """Start the application"""
        self.root.mainloop()


def main():
    app = ImagePathifier()
    app.run()


if __name__ == "__main__":
    main()