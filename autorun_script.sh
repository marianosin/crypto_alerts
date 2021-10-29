
source ~/anaconda3/etc/profile.d/conda.sh
conda activate adam
python3 /media/nuevo_vol/Proyectos/crypto_alerts/price_downloader.py
python3 /media/nuevo_vol/Proyectos/crypto_alerts/strategies_tester.py
conda deactivate
