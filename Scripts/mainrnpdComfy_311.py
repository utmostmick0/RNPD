import os
from IPython.display import clear_output
from subprocess import call, getoutput, Popen, run
import time
import ipywidgets as widgets
import requests
import sys
import fileinput
from torch.hub import download_url_to_file
from urllib.parse import urlparse, parse_qs, unquote
import re
import six

from urllib.request import urlopen, Request
import tempfile
from tqdm import tqdm 




def Deps(force_reinstall):

    if not force_reinstall and os.path.exists('/usr/local/lib/python3.11/dist-packages/gradio'):
        ntbk()
        os.environ['TORCH_HOME'] = '/notebooks/cache/torch'
        os.environ['PYTHONWARNINGS'] = 'ignore'
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
        print('[1;32mModules and notebooks updated, dependencies already installed')

    else:
        call("pip install --root-user-action=ignore --no-deps -q accelerate==0.12.0", shell=True, stdout=open('/dev/null', 'w'))
        call("pip uninstall -qq deepspeed -y", shell=True, stdout=open('/dev/null', 'w'))
        ntbk()
        if not os.path.exists('/models'):
            call('mkdir /models', shell=True)
        if not os.path.exists('/notebooks/models'):
            call('ln -s /models /notebooks', shell=True)
        if os.path.exists('/deps'):
            call("rm -r /deps", shell=True)
        call('mkdir /deps', shell=True)
        if not os.path.exists('cache'):
            call('mkdir cache', shell=True)
        os.chdir('/deps')
        call('wget -q -i https://raw.githubusercontent.com/utmostmick0/fast-stable-diffusion/main/Dependencies/aptdeps_311.txt', shell=True)
        call('dpkg -i *.deb', shell=True, stdout=open('/dev/null', 'w'))
        depsinst("https://github.com/utmostmick0/sd_dependencies/blob/f2216938549c58f6d16363cdbe8650960839bc7e/rnpddeps-t2.tar.zst", "/deps/rnpddeps-t2.tar.zst")
        call('tar -C / --zstd -xf rnpddeps-t2.tar.zst', shell=True, stdout=open('/dev/null', 'w'))
        call("pip install --root-user-action=ignore -q transformers==4.30.2", shell=True, stdout=open('/dev/null', 'w'))
        os.chdir('/notebooks')
        call("git clone --depth 1 -q --branch main https://github.com/utmostmick0/diffusers /diffusers", shell=True, stdout=open('/dev/null', 'w'), stderr=open('/dev/null', 'w'))
        os.environ['TORCH_HOME'] = '/notebooks/cache/torch'
        os.environ['PYTHONWARNINGS'] = 'ignore'
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
        call("sed -i 's@text = _formatwarnmsg(msg)@text =\"\"@g' /usr/lib/python3.11/warnings.py", shell=True)
        if not os.path.exists('/notebooks/diffusers'):
            call('ln -s /diffusers /notebooks', shell=True)
        call("rm -r /deps", shell=True)
        os.chdir('/notebooks')
        clear_output()

        done()




def depsinst(url, dst):
    file_size = None
    req = Request(url, headers={"User-Agent": "torch.hub"})
    u = urlopen(req)
    meta = u.info()
    if hasattr(meta, 'getheaders'):
        content_length = meta.getheaders("Content-Length")
    else:
        content_length = meta.get_all("Content-Length")
    if content_length is not None and len(content_length) > 0:
        file_size = int(content_length[0])

    with tqdm(total=file_size, disable=False, mininterval=0.5,
              bar_format='Installing dependencies |{bar:20}| {percentage:3.0f}%') as pbar:
        with open(dst, "wb") as f:
            while True:
                buffer = u.read(8192)
                if len(buffer) == 0:
                    break
                f.write(buffer)
                pbar.update(len(buffer))
            f.close()
            
            

def dwn(url, dst, msg):
    file_size = None
    req = Request(url, headers={"User-Agent": "torch.hub"})
    u = urlopen(req)
    meta = u.info()
    if hasattr(meta, 'getheaders'):
        content_length = meta.getheaders("Content-Length")
    else:
        content_length = meta.get_all("Content-Length")
    if content_length is not None and len(content_length) > 0:
        file_size = int(content_length[0])

    with tqdm(total=file_size, disable=False, mininterval=0.5,
              bar_format=msg+' |{bar:20}| {percentage:3.0f}%') as pbar:
        with open(dst, "wb") as f:
            while True:
                buffer = u.read(8192)
                if len(buffer) == 0:
                    break
                f.write(buffer)
                pbar.update(len(buffer))
            f.close()

            
            

def ntbk():

    os.chdir('/notebooks')
    if not os.path.exists('Latest_Notebooks'):
        call('mkdir Latest_Notebooks', shell=True)
    else:
        call('rm -r Latest_Notebooks', shell=True)
        call('mkdir Latest_Notebooks', shell=True)
    os.chdir('/notebooks/Latest_Notebooks')
    call('wget -q -i https://github.com/utmostmick0/RNPD/blob/eb562416cbb951e6f665638b9a605d7201640814/Notebooks.txt', shell=True)
    call('rm Notebooks.txt', shell=True)
    os.chdir('/notebooks')
    

    
    
def repo():
    
    os.chdir('/notebooks')

    print('[1;33mInstalling/Updating the repo...')
    os.chdir('/notebooks')
    if not os.path.exists('ComfyUI'):
        call('git clone -q --depth 1 https://github.com/comfyanonymous/ComfyUI', shell=True)

    os.chdir('ComfyUI')
    call('git reset --hard', shell=True)
    print('[1;32m')
    call('git pull', shell=True)
    os.chdir('/notebooks')
    clear_output()
    done()



def mdls(Original_Model_Version, Path_to_MODEL, MODEL_LINK, Temporary_Storage=False):

    import gdown
   
    src=getsrc(MODEL_LINK)


    call('ln -s /datasets/stable-diffusion-classic/SDv1.5.ckpt /notebooks/ComfyUI/models/checkpoints', shell=True, stdout=open('/dev/null', 'w'), stderr=open('/dev/null', 'w'))
    call('ln -s /datasets/stable-diffusion-v2-1-base-diffusers/stable-diffusion-2-1-base/v2-1_512-nonema-pruned.safetensors /notebooks/ComfyUI/models/checkpoints', shell=True, stdout=open('/dev/null', 'w'), stderr=open('/dev/null', 'w'))
    call('ln -s /datasets/stable-diffusion-v2-1/stable-diffusion-2-1/v2-1_768-nonema-pruned.safetensors /notebooks/ComfyUI/models/checkpoints', shell=True, stdout=open('/dev/null', 'w'), stderr=open('/dev/null', 'w'))
    call('ln -s /datasets/stable-diffusion-xl/sd_xl_base_1.0.safetensors /notebooks/ComfyUI/models/checkpoints', shell=True, stdout=open('/dev/null', 'w'), stderr=open('/dev/null', 'w'))

    if Path_to_MODEL !='':
      if os.path.exists(str(Path_to_MODEL)):
        print('[1;32mUsing the custom model.')
        model=Path_to_MODEL
      else:
          print('[1;31mWrong path, check that the path to the model is correct')

    elif MODEL_LINK !="":
         
      if src=='civitai':
         modelname=get_name(MODEL_LINK, False)
         if Temporary_Storage:
            model=f'/models/{modelname}'
         else:
            model=f'/notebooks/ComfyUI/models/checkpoints/{modelname}'
         if not os.path.exists(model):
            dwn(MODEL_LINK, model, 'Downloading the custom model')
            clear_output()
         else:
            print('[1;33mModel already exists')
      elif src=='gdrive':
         modelname=get_name(MODEL_LINK, True)
         if Temporary_Storage:
            model=f'/models/{modelname}'
         else:
            model=f'/notebooks/ComfyUI/models/checkpoints/{modelname}'
         if not os.path.exists(model):
            gdown.download(url=MODEL_LINK, output=model, quiet=False, fuzzy=True)
            clear_output()
         else:
            print('[1;33mModel already exists')
      else:
         modelname=os.path.basename(MODEL_LINK)
         if Temporary_Storage:
            model=f'/models/{modelname}'
         else:
            model=f'/notebooks/ComfyUI/models/checkpoints/{modelname}'
         if not os.path.exists(model):
            gdown.download(url=MODEL_LINK, output=model, quiet=False, fuzzy=True)
            clear_output()
         else:
            print('[1;33mModel already exists')

      if os.path.exists(model) and os.path.getsize(model) > 1810671599:
        print('[1;32mModel downloaded, using the custom model.')
      else:
        call('rm '+model, shell=True, stdout=open('/dev/null', 'w'), stderr=open('/dev/null', 'w'))
        print('[1;31mWrong link, check that the link is valid')

    else:
        if Original_Model_Version == "v1.5":
           model="/notebooks/ComfyUI/models/checkpoints/SDv1.5.ckpt"
           print('[1;32mUsing the original V1.5 model')
        elif Original_Model_Version == "v2-512":
            model="/notebooks/ComfyUI/models/checkpoints/v2-1_512-nonema-pruned.safetensors"
            print('[1;32mUsing the original V2-512 model')
        elif Original_Model_Version == "v2-768":
           model="/notebooks/ComfyUI/models/checkpoints/v2-1_768-nonema-pruned.safetensors"
           print('[1;32mUsing the original V2-768 model')
        elif Original_Model_Version == "SDXL":
            model="/notebooks/ComfyUI/models/checkpoints/sd_xl_base_1.0.safetensors"
            print('[1;32mUsing the original SDXL model')
        else:
            model="/notebooks/ComfyUI/models/checkpoints"
            print('[1;31mWrong model version, try again')
    try:
        model
    except:
        model="/notebooks/ComfyUI/models/checkpoints"

    return model



def loradwn(LoRA_LINK):

    import gdown

    if LoRA_LINK=='':
        print('[1;33mNothing to do')
    else:
        src=getsrc(LoRA_LINK)

        if src=='civitai':
            modelname=get_name(LoRA_LINK, False)
            loramodel=f'/notebooks/ComfyUI/models/loras/{modelname}'
            if not os.path.exists(loramodel):
              dwn(LoRA_LINK, loramodel, 'Downloading the LoRA model')
              clear_output()
            else:
              print('[1;33mModel already exists')
        elif src=='gdrive':
            modelname=get_name(LoRA_LINK, True)
            loramodel=f'/notebooks/ComfyUI/models/loras/{modelname}'
            if not os.path.exists(loramodel):
              gdown.download(url=LoRA_LINK, output=loramodel, quiet=False, fuzzy=True)
              clear_output()
            else:
              print('[1;33mModel already exists')
        else:
            modelname=os.path.basename(LoRA_LINK)
            loramodel=f'/notebooks/ComfyUI/models/loras/{modelname}'
            if not os.path.exists(loramodel):
              gdown.download(url=LoRA_LINK, output=loramodel, quiet=False, fuzzy=True)
              clear_output()
            else:
              print('[1;33mModel already exists')

        if os.path.exists(loramodel) :
          print('[1;32mLoRA downloaded')
        else:
          print('[1;31mWrong link, check that the link is valid')



def CNet(ControlNet_Model, ControlNet_XL_Model):
    
    def download(url, model_dir):

        filename = os.path.basename(urlparse(url).path)
        pth = os.path.abspath(os.path.join(model_dir, filename))
        if not os.path.exists(pth):
            print('Downloading: '+os.path.basename(url))
            download_url_to_file(url, pth, hash_prefix=None, progress=True)
        else:
          print(f"[1;32mThe model {filename} already exists[0m")    

    wrngv1=False
    mdldir="/notebooks/ComfyUI/models/controlnet"
    for filename in os.listdir(mdldir):
      if "_sd14v1" in filename:
        renamed = re.sub("_sd14v1", "-fp16", filename)
        os.rename(os.path.join(mdldir, filename), os.path.join(mdldir, renamed))

    call('wget -q -O CN_models.txt https://github.com/utmostmick0/fast-stable-diffusion/raw/main/AUTOMATIC1111_files/CN_models.txt', shell=True)
    call('wget -q -O CN_models_XL.txt https://github.com/utmostmick0/fast-stable-diffusion/raw/main/AUTOMATIC1111_files/CN_models_XL.txt', shell=True)
      
    with open("CN_models.txt", 'r') as f:
        mdllnk = f.read().splitlines()
    with open("CN_models_XL.txt", 'r') as d:
        mdllnk_XL = d.read().splitlines()
    call('rm CN_models.txt CN_models_XL.txt', shell=True)
      
    os.chdir('/notebooks')    
    if ControlNet_Model == "All" or ControlNet_Model == "all" :     
      for lnk in mdllnk:
          download(lnk, mdldir)
      clear_output()

    elif ControlNet_Model == "15":
      mdllnk=list(filter(lambda x: 't2i' in x, mdllnk))
      for lnk in mdllnk:
          download(lnk, mdldir)
      clear_output()        


    elif ControlNet_Model.isdigit() and int(ControlNet_Model)-1<14 and int(ControlNet_Model)>0:
      download(mdllnk[int(ControlNet_Model)-1], mdldir)
      clear_output()
      
    elif ControlNet_Model == "none":
       pass
       clear_output()

    else:
      print('[1;31mWrong ControlNet V1 choice, try again')
      wrngv1=True


    if ControlNet_XL_Model == "All" or ControlNet_XL_Model == "all" :
      for lnk_XL in mdllnk_XL:
          download(lnk_XL, mdldir)
      if not wrngv1:
        clear_output()
      done()

    elif ControlNet_XL_Model.isdigit() and int(ControlNet_XL_Model)-1<5:
      download(mdllnk_XL[int(ControlNet_XL_Model)-1], mdldir)
      if not wrngv1:
        clear_output()
      done()
    
    elif ControlNet_XL_Model == "none":
       pass
       if not wrngv1:
        clear_output()
       done()       

    else:
      print('[1;31mWrong ControlNet V2 choice, try again')



def sd():
   
    localurl="https://tensorboard-"+os.environ.get('PAPERSPACE_FQDN')
    call("sed -i 's@logging.info(\"To see the GUI go to: {}://{}:{}\".format(scheme, address, port))@print(\"[32m\u2714 Connected\")\\n            print(\"[1;34m"+localurl+"[0m\")@' /notebooks/ComfyUI/server.py", shell=True)
    os.chdir('/notebooks')

      


def getsrc(url):
    parsed_url = urlparse(url)
    if parsed_url.netloc == 'civitai.com':
        src='civitai'
    elif parsed_url.netloc == 'drive.google.com':
        src='gdrive'
    elif parsed_url.netloc == 'huggingface.co':
        src='huggingface'
    else:
        src='others'
    return src



def get_name(url, gdrive):

    from gdown.download import get_url_from_gdrive_confirmation

    if not gdrive:
        response = requests.get(url, allow_redirects=False)
        if "Location" in response.headers:
            redirected_url = response.headers["Location"]
            quer = parse_qs(urlparse(redirected_url).query)
            if "response-content-disposition" in quer:
                disp_val = quer["response-content-disposition"][0].split(";")
                for vals in disp_val:
                    if vals.strip().startswith("filename="):
                        filenm=unquote(vals.split("=", 1)[1].strip())
                        return filenm.replace("\"","")
    else:
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"}
        lnk="https://drive.google.com/uc?id={id}&export=download".format(id=url[url.find("/d/")+3:url.find("/view")])
        res = requests.session().get(lnk, headers=headers, stream=True, verify=True)
        res = requests.session().get(get_url_from_gdrive_confirmation(res.text), headers=headers, stream=True, verify=True)
        content_disposition = six.moves.urllib_parse.unquote(res.headers["Content-Disposition"])
        filenm = re.search(r"filename\*=UTF-8''(.*)", content_disposition).groups()[0].replace(os.path.sep, "_")
        return filenm




def done():
    done = widgets.Button(
        description='Done!',
        disabled=True,
        button_style='success',
        tooltip='',
        icon='check'
    )
    display(done)
