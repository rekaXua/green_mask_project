# green_mask_project
Applying mask on mosaic censorship using openCV. Meant to work in tandem with [DeepCreamPy](https://github.com/deeppomf/DeepCreamPy)

[![GitHub issues](https://img.shields.io/github/issues/rekaXua/green_mask_project.svg?label=Issues)](https://github.com/rekaXua/green_mask_project/issues)
[![GitHub downloads](https://img.shields.io/github/downloads/rekaXua/green_mask_project/total.svg?label=Downloads)](https://github.com/rekaXua/green_mask_project/releases)
[![GitHub release](https://img.shields.io/github/release/rekaXua/green_mask_project.svg?label=Version)](https://github.com/rekaXua/green_mask_project/releases/latest)
[![Twitter Follow](https://img.shields.io/twitter/follow/Alexander_rekaX.svg?label=Alexander_rekaX&style=flat&logo=twitter)](https://twitter.com/Alexander_rekaX/)
[![Donate with PayPal](https://img.shields.io/badge/PayPal-Donate-gray.svg?logo=paypal&label=)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=PDS9QQPVNUERE)

**Don't forget to install python3 and all the requirements with command "pip3 install -r green_mask_project/requirements.txt" in cmd or bash**
<p align="center">
  <img src="https://github.com/rekaxua/green_mask_project/blob/master/decensor_input_original/asuka.png" width="400">
  <img src="https://github.com/rekaxua/green_mask_project/blob/master/decensor_input/asuka.png" width="400">
</p>

**Picture above was made with default values. DCP can easily work with them, but if your usage requires more precision, you can try to make results better by playing with the settings*

**TODO:**
- GUI
- Better detection algorithm
- ~~Fix DCP problems with transparency~~


>To integrate this with DeepCreamPy - just extract this project in DCP folder and add "python3 decensor.py --is_mosaic=True" to start.bat / .sh
