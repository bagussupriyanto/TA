import time
import os
import flet as ft
import tkinter as tk
from tkinter import messagebox

from main import AESalgo

# from backend_aes import AESalgoritma

def main(page: ft.Page):

    # !-----------------------------------------Windows Sett
    
    page.window_always_on_top = True
    page.window_maximizable = False
    page.window_maximized = False
    page.window_full_screen = False
    page.window_resizable = False
    
    page.window_left = 1100
    page.window_top = 25

    page.window_width = 470
    page.window_height = 900

    page.window_max_height = 900
    page.window_max_width = 470

    page.window_min_height = 900
    page.window_min_width = 470

    page.theme_mode = "LIGHT"

    page.title = "SMPN 11 BINTAN - Aplikasi Enkripsi & Dekripsi AES"

    page.bgcolor = "white"
    page.spacing = 0
    page.padding = 0

    page.fonts = {
        "Poppins Reg" : "/fonts/Poppins-Regular.ttf",
        "Poppins Semi" : "/fonts/Poppins-SemiBold.ttf",
    }

    def open_dlg(e):
        page.dialog = firstPopup
        firstPopup.open = True
        page.update()

    def close_dlg(e):
        firstPopup.open = False
        page.update()

    firstPopup = ft.AlertDialog(
        actions=[
            ft.Container(
                height=15,
            ),
            ft.Container(
                alignment=ft.alignment.center,
                content= ft.Text(
                    size=20,
                    value="HAI, SELAMAT DATANG",
                    text_align=ft.TextAlign.CENTER,
                    weight=ft.FontWeight.BOLD,
                )
            ),
            ft.Container(
                alignment=ft.alignment.center,
                content= ft.Text(
                    size=15,
                    value="Aplikasi Enkripsi dan Dekripsi file ini menggunakan algoritma Advanced Encryption Standard (AES) untuk mengamankan file nilai ijazah siswa",
                    text_align=ft.TextAlign.CENTER,
                )
            ),
            ft.Container(
                height=15,
            ),
            ft.Container(
                alignment=ft.alignment.center,
                content= ft.Image(src=f"/images/popup.png",)
            ),
            ft.ElevatedButton(
                text="Tutup",
                on_click=close_dlg,
                data=0,
            ),
        ],
    )

    open_dlg(None)

    # !----------------------------------------Back End

     # !-----------------------------YANG MENGATUR BAGIAN FILE PICKER------------------------------
    # Function untuk memilih file
    def select_file(e: ft.FilePickerResultEvent):
        page.add(filepicker)
        filepicker.pick_files("Pilih File")

    #Function untuk mengubah value dari variable file_path,dan mengambil string directory file
    file_path = ft.Text(
        value="Pilih File...",
        size=14,
        color="0xFF302f41",
        font_family="Poppins Regu",
        text_align= ft.TextAlign.CENTER,
    )
    
    icon_path = ft.Image(src=f"/icons/mdi_file-document-add-outline.png",height=34,)
    fileIconContainer = ft.Column(
        controls= [
            icon_path,
            file_path,
        ],
        alignment= ft.MainAxisAlignment.CENTER,
        horizontal_alignment= ft.CrossAxisAlignment.CENTER,
    )

    def return_file(e: ft.FilePickerResultEvent):  
        file_path.value = e.files[0].path
        changeicon = True
        iconValue = "/icons/material-symbols_file-present-rounded.png"
        icon_path.src =f"${iconValue}"
        print(file_path.value)
        print(changeicon)
        print(iconValue)
        file_path.update()
        icon_path.update()
        out_file =  file_path.value
        print(out_file)

    filepicker = ft.FilePicker(on_result=return_file)

    dlg_pass = ft.AlertDialog(
        actions=[
            ft.Container(
                height=20,
            ),
            ft.Container(
                alignment=ft.alignment.center,
                content= ft.Image(src=f"/icons/material-symbols_warning-rounded.png",height=34,)
            ),
            ft.Text(
                value= "Mohon Masukan Key Terlebih dahulu.",
                text_align=ft.TextAlign.CENTER,
            )
        ],
    )

    dlg_file = ft.AlertDialog(
        actions=[
            ft.Container(
                height=20,
            ),
            ft.Container(
                alignment=ft.alignment.center,
                content= ft.Image(src=f"/icons/material-symbols_warning-rounded.png",height=34,)
            ),
            ft.Text(
                value="Mohon Pilih File Terlebih dahulu.",
                text_align=ft.TextAlign.CENTER,
            )
        ],
    )

    dlg_file_enripted = ft.AlertDialog(
        actions=[
            ft.Container(
                height=20,
            ),
            ft.Container(
                alignment=ft.alignment.center,
                content= ft.Image(src=f"/icons/material-symbols_warning-rounded.png",height=34,)
            ),
            ft.Text(
                value="File yang sudah di Enkripsi tidak bisa di Enkripsi lagi",
                text_align=ft.TextAlign.CENTER,
            )
        ],
    )

    dlg_file_decripted = ft.AlertDialog(
        actions=[
            ft.Container(
                height=20,
            ),
            ft.Container(
                alignment=ft.alignment.center,
                content= ft.Image(src=f"/icons/material-symbols_warning-rounded.png",height=34,)
            ),
            ft.Text(
                value="File yang belum di Enkripsi tidak bisa di Dekripsi",
                text_align=ft.TextAlign.CENTER,
            )
        ],
    )

    dlg_finish = ft.AlertDialog(
        actions=[
            ft.Container(
                height=20,
            ),
            ft.Container(
                alignment=ft.alignment.center,
                content= ft.Image(src=f"/icons/material-symbols_check-circle-rounded.png",height=34,)
            ),
            ft.Container(
                alignment=ft.alignment.center,
                content= ft.Text(
                    value="Selesai.",
                    text_align=ft.TextAlign.CENTER,
                )
            ),
            
        ],
    )

    

    algoritmaAES = AESalgo()
    
    def enc_click(e):
        if file_path.value == "Pilih File...":
            page.dialog = dlg_file
            dlg_file.open = True
            page.update()
        
        elif not pass_field.value:
            page.dialog = dlg_pass
            dlg_pass.open = True
            page.update()
        else:
            value_password = pass_field.value
            if( ".Encrypted" in file_path.value):
                page.dialog = dlg_file_enripted
                dlg_file_enripted.open = True
                page.update()
            else:
                out_file_name = os.path.basename(file_path.value)
                out_file_path = file_path.value.replace(out_file_name, "Hasil Enkripsi/")
                out_file = out_file_name + ".Encrypted"
                
                isExist = os.path.exists(out_file_path)
                if not isExist:
                    os.makedirs(out_file_path)
                
                out_file_encrypted = out_file_path + out_file
                start = time.time()
                print ('Encrypting', file_path.value, 'to', out_file_encrypted)
                algoritmaAES.encrypt_file( file_path.value, out_file_encrypted, value_password)
                end = time.time()
                print('Selesai')
                print('Time',end - start,'s')
                file_path.value = "Pilih File..."
                icon_path.src = f"/icons/mdi_file-document-add-outline.png"
                pass_field.value = None
                pass_field.update()
                file_path.update()
                icon_path.update()
                page.dialog = dlg_finish
                dlg_finish.open = True
            page.update()
    

    def dec_click(e):
        if file_path.value == "Pilih File...":
            page.dialog = dlg_file
            dlg_file.open = True
            page.update()
        
        elif not pass_field.value:
            page.dialog = dlg_pass
            dlg_pass.open = True
            page.update()

        else:
            if(".Encrypted" not in file_path.value):
                page.dialog = dlg_file_decripted
                dlg_file_decripted.open = True
                page.update()
            else:
                value_password = pass_field.value
                print(value_password)
                out_file = file_path.value.replace('.Encrypted','')
                print(out_file)
                start = time.time()
                print ('Dekrypting', file_path.value, 'to', out_file)
                algoritmaAES.decrypt_file( file_path.value, out_file, value_password)
                end = time.time()
                print('Selesai')
                print('Time',end - start,'s')
                file_path.value = "Pilih File..."
                icon_path.src = f"/icons/mdi_file-document-add-outline.png"
                pass_field.value = None
                pass_field.update()
                file_path.update()
                icon_path.update()
                page.dialog = dlg_finish
                dlg_finish.open = True
                page.update()
    
    def help_click(e):
        page.dialog = help_1
        help_1.open = True
        page.update()

    def next_click(e):
        page.dialog = help_2
        help_2.open = True
        page.update()

    def next_click1(e):
        page.dialog = help_3
        help_3.open = True
        page.update()

    def close_help(e):
        help_3.open = False
        page.update()

    help_1 = ft.AlertDialog(
        actions=[
            ft.Container(
                height=15,
            ),
            ft.Container(
                alignment=ft.alignment.center,
                content= ft.Text(
                    size=17,
                    value="Apa itu Advanced Encryption Standard (AES)?",
                    text_align=ft.TextAlign.JUSTIFY,
                    weight=ft.FontWeight.W_700,
                )
            ),
            ft.Container(
                height=15,
            ),
            ft.Container(
                alignment=ft.alignment.center,
                content= ft.Text(
                    value="Advanced Encryption Standard (AES) algoritma adalah salah satu enkripsi blok chiper algoritma yang diterbitkan oleh National Institute Standar dan Teknologi (NIST) pada tahun 2000. Tujuan utama dari algoritma ini adalah untuk menggantikan beberapa aspek yang rentan pada Algoritman DES.",
                    text_align=ft.TextAlign.JUSTIFY,
                )
            ),
            ft.Divider(),
            ft.ElevatedButton(
                text="Selanjutnya",
                on_click=next_click,
                data=0,
            ),
        ],
    )

    help_2 = ft.AlertDialog(
        actions=[
            ft.Container(
                height=15,
            ),
            ft.Container(
                alignment=ft.alignment.center,
                content= ft.Text(
                    size=17,
                    value="Proses AES 128",
                    text_align=ft.TextAlign.CENTER,
                )
            ),
            ft.Container(
                height=15,
            ),
            ft.Container(
                alignment=ft.alignment.center,
                content= ft.Image(src=f"/images/proses.png",)
            ),
            ft.Container(
                height=15,
            ),
            ft.Divider(),
            ft.ElevatedButton(
                text="Selanjutnya",
                on_click=next_click1,
                data=0,
            ),
        ],
    )

    help_3 = ft.AlertDialog(
        actions=[
            ft.Container(
                height=15,
            ),
            ft.Container(
                alignment=ft.alignment.center,
                content= ft.Text(
                    size=17,
                    value="Cara Penggunaan",
                    text_align=ft.TextAlign.CENTER,
                )
            ),
            ft.Divider(),
            ft.Text(
                value="1. Pilih File yang akan di Enkripsi atau Dekripsi\n2. Masukan Key yang akan digunakan untuk Enkripsi atau Dekripsi(Key Harus Sama)\n3. Klik tombol Enkripsi atau Dekripsi\n4.Hasil Enkripsi atau Dekripsi Berada dimana File awal untuk di enkripsi diambil",
                text_align=ft.TextAlign.LEFT,
            ),
            ft.Divider(),
            ft.ElevatedButton(
                text="Tutup",
                on_click=close_help,
                data=0,
            ),
        ],
    )


    # !----------------------------------------List Component Widget
    banner_image = ft.Container(
        width=460,
        height=150,
        border_radius= ft.border_radius.all(10),
        image_src=f"/images/bg-top.png",
        image_fit= ft.ImageFit.COVER,
        margin=ft.margin.symmetric(horizontal=16),
        padding=ft.padding.symmetric(vertical=11,horizontal=66),
        content=ft.Image(
            src="assets/images/icon.png",
            height=81,
            width=81,
        )
    )

    tittle_container = ft.Container(
        width=450,
        height=35,
        border_radius=ft.border_radius.all(10),
        bgcolor= "0xFF302f41",
        margin=ft.margin.symmetric(horizontal=16),
        padding=ft.padding.symmetric(vertical=9,horizontal=0),
        alignment=ft.alignment.center,
        content=ft.Text(
            value="APLIKASI ENKRIPSI & DEKRIPSI AES",
            size=16,
            color= "0xFFFFFFFF",
            font_family="Poppins Semi",
        ),
    )

    pick_file_btn = ft.Container(
        width=450,
        height=115,
        border= ft.border.all(width=2,color="0xFF302f41"),
        border_radius=ft.border_radius.all(10),
        bgcolor= "transparent",
        margin=ft.margin.symmetric(horizontal=16),
        padding=ft.padding.symmetric(vertical=9,horizontal=0),
        content= fileIconContainer,
        on_click=select_file,
    )

    def hide_label(event):
        label.visible = False

    def show_label(event):
        label.visible = True

    label = ft.Text(
        value="  Masukkan Key",
    )

    pass_field = ft.TextField(
        border=ft.InputBorder.NONE,
        password=True,
        can_reveal_password=True,
        on_focus=hide_label,
        on_blur=show_label,
    )

    pass_input_field = ft.Container(
        width=450,
        height= 38,
        border= ft.border.all(width=2,color="0xFF302f41",),
        margin=ft.margin.symmetric(horizontal=16),
        border_radius=ft.border_radius.all(10),
        padding=ft.padding.symmetric(vertical=8),
        bgcolor= "white",
        content=ft.Row([label, pass_field]),
    )

    enc_btn = ft.Container(
        width=450,
        height=38,
        border_radius=ft.border_radius.all(10),
        bgcolor= "0xFF302f41",
        margin=ft.margin.symmetric(horizontal=16),
        padding=ft.padding.symmetric(vertical=9,),
        content=ft.Row(
            [
                ft.Image(
                    src=f"/icons/mdi_archive-lock.png",
                    height=17,
                ),
                ft.Text(
                    value="Enkripsi File",
                    size=11,
                    color= "0xFFFFFFFF",
                    font_family="Poppins Regu",
                ),
            ],
            
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        on_click= enc_click,
    )

    dec_btn = ft.Container(
        width=450,
        height=38,
        border= ft.border.all(width=2,color="0xFF302f41",),
        border_radius=ft.border_radius.all(10),
        bgcolor= "0xFFFFFFFF",
        margin=ft.margin.symmetric(horizontal=16),
        padding=ft.padding.symmetric(vertical=9,),
        alignment=ft.alignment.center,
        content=ft.Row(
            [
                ft.Image(
                    src=f"/icons/mdi_archive-lock-open.png",
                    height=17,
                ),
                ft.Text(
                    value="Dekripsi File",
                    size=11,
                    color= "0xFF302f41",
                    font_family="Poppins Regu",
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        on_click=dec_click,
    )

    bottom_banner_image = ft.Image(
        src=f"/images/bg-bottom.png",
    )

    help_btn = ft.Container(
        width=38,
        height=38,
        border_radius=ft.border_radius.all(10),
        bgcolor= "0xFF302f41",
        margin=ft.margin.only(left=394),
        padding=ft.padding.symmetric(vertical=9,),
        alignment=ft.alignment.bottom_right,
        content=ft.Row(
            [
                ft.Text(
                    value="?",
                    size=11,
                    color= "0xFFFFFFFF",
                    font_family="Poppins Regu",
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        on_click= help_click,
    )


    # !----------------------------------------Front End

    scafold = ft.Column(
        [
            ft.Container(
                height=16,
            ),
            banner_image,
            ft.Container(
                height=10,
            ),
            tittle_container,
            ft.Container(
                height=10,
            ),
            pick_file_btn,
            ft.Container(
                height=10,
            ),
            ft.Container(
                margin=ft.margin.symmetric(horizontal=16),
                content= ft.Text(
                    value="",
                    size=11,
                    color="0xFF302f41",
                    font_family="Poppins Semi",
                ),
            ),
            ft.Container(
                height=10,
            ),
            pass_input_field,
            ft.Container(
                height=15,
            ),
            enc_btn,
            ft.Container(
                height=5,
            ),
            dec_btn,
            ft.Container(
                height=3,
                image_src=f"/images/icon.png",
            ),
        ],
        spacing=0,
    )

    page.add(
        scafold,
        ft.Container(
            height=10,
        ),
        help_btn,
        bottom_banner_image,
    )

ft.app(
    target=main,
    assets_dir="assets"
    
)
