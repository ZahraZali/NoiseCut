{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "423b5dce-48b8-4431-abfc-f96519d27c98",
   "metadata": {},
   "outputs": [],
   "source": [
    "#!/bin/bash\n",
    "\n",
    "set -e\n",
    "\n",
    "rm -rf data\n",
    "wget -r https://owlpy.org/examples/data/ -nv -e 'robots=off' -R 'index.html' --no-parent -nH --cut-dirs=2 -P data\n",
    "find data -name '*.tmp' -print0 | xargs -0 rm"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
