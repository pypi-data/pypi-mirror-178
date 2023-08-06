---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.1
kernelspec:
  language: python
  name: python3
---

# Usage

Pymech is a simple interface to read / to write Nek5000 and SIMSON specific
data files to / from the Python world. With this capability you could:

- make publication-quality figures
- post-process
- manipulate meshes
- generate initial conditions
- interpolate or extrapolate solution fields, and

possibly many more potential use-cases  -- the limit is your imagination! Here
we look at some simple operations you can do. Start by [installing
pymech](index.rst) and:

```{code-cell} ipython3
!git clone --recursive https://github.com/eX-Mech/pymech.git
%cd pymech/tests/data/nek
```

## {class}`pymech.neksuite`

```{code-cell} ipython3
from pymech.neksuite import readnek

field = readnek('channel3D_0.f00001')
```

Simply typing the read `field` would give you some basic information:

```{code-cell} ipython3
field
```

### {class}`pymech.core.HexaData`

+++

The {class}`pymech.core.HexaData` class is the in-memory data structure widely used in Pymech. It stores a description of the field and other metadata. Let's look at the available attributes:

```{code-cell} ipython3
[attr for attr in dir(field) if not attr.startswith('__')]
```

Here `check_connectivity` and `merge` are methods, and `elem` and `elmap` are data objects. The rest of the attributes store metadata. See {ref}`core` to understand what they imply.

```{code-cell} ipython3
print(field.endian, field.istep, field.lr1, field.nbc, field.ncurv, field.ndim, field.nel, field.time, field.var, field.wdsz)
```

The `elem` attribute contains data of physical fields. It is an array of lists, with each array representing an element.

```{code-cell} ipython3
print("There are", field.nel, "elements in this file")
```

### {class}`pymech.core.Elem`

The raw arrays are stored as a list of {class}`pymech.core.Elem` instances as {class}`pymech.core.HexaData`'s `elem` attribute.

```{code-cell} ipython3
first_element = field.elem[0]
print("Type =", type(first_element))
print(first_element)
```

Let us look at the attributes of an element

```{code-cell} ipython3
[attr for attr in dir(first_element) if not attr.startswith('__')]
```

Except for the following attributes of an element object

```{code-cell} ipython3
print(first_element.bcs, first_element.ccurv, first_element.curv)
```

it contains large arrays

```{code-cell} ipython3
print("Shape of element velocity and pressure arrays = ", first_element.vel.shape, first_element.pres.shape)
```

## {mod}`pymech.dataset`

```{code-cell} ipython3
from pymech.dataset import open_dataset

ds = open_dataset('channel3D_0.f00001')
```

This function loads the field file in a more convenient [xarray](https://xarray.pydata.org) dataset.

```{code-cell} ipython3
ds
```

The dataset is more descriptive and useful for exploratory work, such as post-processing and plotting.

+++

### Computing statistics

+++

Calculate median for all variables

```{code-cell} ipython3
ds.median()
```

### Slicing

+++

Slice by index:

```{code-cell} ipython3
ds.ux.isel(z=32)
```

It is also possible to slice by value using `sel` method

+++

### Visualizing

+++

Average in spanwise (`z`) direction and plot velocity profile

```{code-cell} ipython3
ds.ux.mean('z').plot()
```

Average in both horizontal direction and plot 1D profile

```{code-cell} ipython3
ds_1d = ds.mean(['x', 'z'])
ds_1d.ux.plot()
```

It is also worth knowing that it is possible to:

- Parallelize these operations using `ds.chunk` method followed by `ds.compute`
- Open a multiple files into a single dataset using {any}`pymech.dataset.open_mfdataset`, optionally in parallel.

Read the [xarray documentation](https://xarray.pydata.org/en/stable/quick-overview.html) to see how to use them.
