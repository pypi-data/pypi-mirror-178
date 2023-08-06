GPUs
====

Quickstart
----------

Coiled supports running computations with GPU-enabled machines. You can first create a Coiled software environment using the RAPIDS image, publicly available on Docker Hub (see the `RAPIDS image <https://hub.docker.com/r/rapidsai/rapidsai-core>`_):

.. code-block:: python

    import coiled

    coiled.create_software_environment(
        name="rapids-stable",
        container="rapidsai/rapidsai-core:22.10-cuda11.5-runtime-ubuntu20.04-py3.9",
    )

Then you can create a cluster with GPU-enabled machines by using the ``worker_gpu`` argument:

.. code-block:: python

    cluster = coiled.Cluster(
        software="rapids-stable",
        n_workers=4,
        scheduler_gpu=True,  # recommended
        worker_gpu=1,  # single T4 per worker
        worker_class="dask_cuda.CUDAWorker",  # recommended
        use_best_zone=True,  # optional, makes it more likely you'll get a GPU
        environ={"DISABLE_JUPYTER": "true"},  # needed for "stable" RAPIDS image
    )

You'll notice a few arguments we recommend, but are not required:

- ``scheduler_gpu=True`` supports Dask's (de)serialization
- ``worker_class='dask_cuda.CUDAWorker'`` can be helpful if you're using multiple GPUs per worker
- ``use_best_zone=True`` lets the cloud provider pick the zone (in your region) with the best availability for the requested GPU instances
- ``environ={'DISABLE_JUPYTER': 'true'}`` is only needed if you are using the stable RAPIDS image and disables the default Jupyter server from starting

.. _gpu-type:

Requesting Instance Types
-------------------------

When creating a cluster, specifying ``worker_gpu=1`` will default to requesting a g4dn.xlarge (NVIDIA T4) instance type if you are using AWS or n1-standard-4 if you're using Google Cloud. You can also request specific instance types, including multiple GPUs per worker.

AWS
~~~

If you are using AWS, you can request a specific instance type with the ``worker_vm_types`` keyword argument. For example, you could request the p3.8xlarge instance type with 4 GPUs:

.. code-block:: python

    cluster = coiled.Cluster(
        software="rapids-stable",
        n_workers=4,
        scheduler_gpu=True,  # recommended
        worker_vm_types=["p3.8xlarge"],  # four NVIDIA V100s per worker
        worker_class="dask_cuda.CUDAWorker",
        use_best_zone=True,  # optional, makes it more likely you'll get a GPU
        environ={"DISABLE_JUPYTER": "true"},  # needed for "stable" RAPIDS image
    )

.. note::

    AWS users can run into availability issues when requesting GPU-enabled instances, which is why we recommend using ``use_best_zone=True``.

Google Cloud
~~~~~~~~~~~~

If you are using Google Cloud, you can request specific instance types using the
``worker_gpu`` and the ``worker_vm_types``
keyword arguments. You need both arguments since Google Cloud
adds GPUs to different instances (the one exception being 
A100, which is bundled with instance type a2-highgpu-1g).
See the `Google Cloud documentation on GPUs <https://cloud.google.com/compute/docs/gpus>`_
for more details. You will also need to use an instance type from the
`N1 machine series <https://cloud.google.com/compute/docs/general-purpose-machines#n1_machines>`_.

You can request a cluster with two T4 GPUs per worker:

.. code-block:: python

    cluster = coiled.Cluster(
        software="rapids-stable",
        n_workers=2,
        scheduler_gpu=True,  # recommended
        worker_gpu=2,  # two T4s per worker
        worker_class="dask_cuda.CUDAWorker",
        use_best_zone=True,  # optional, makes it more likely you'll get a GPU
        environ={"DISABLE_JUPYTER": "true"},  # needed for "stable" RAPIDS image
    )

Or use ``worker_vm_types`` to specifically request two A100 GPUs per worker:

.. code-block:: python

    cluster = coiled.Cluster(
        software="rapids-stable",
        n_workers=2,
        scheduler_gpu=True,  # recommended
        worker_vm_types=["a2-highgpu-2g"],  # two A100s per worker
        worker_class="dask_cuda.CUDAWorker",
        use_best_zone=True,  # optional, makes it more likely you'll get a GPU
        environ={"DISABLE_JUPYTER": "true"},  # needed for "stable" RAPIDS image
    )


Software Environments
---------------------

When using GPU-enabled machines, you'll also need a software environment that supports GPU-accelerated libraries (PyTorch, RAPIDS, XGBoost, Numba) and the `NVIDIA CUDA Toolkit <https://developer.nvidia.com/cuda-toolkit>`_ for low-level compute optimization. We recommend using the publicly available `RAPIDS image <https://hub.docker.com/r/rapidsai/rapidsai-core>`_, but you can use any software environment that works for you.

Testing
-------

You can test this cluster is working as expected with the following:

.. code-block:: python

    from dask.distributed import Client


    def test_gpu():
        import numpy as np
        import cupy as cp

        x = cp.arange(6).reshape(2, 3).astype("f")
        result = x.sum()
        return cp.asnumpy(result), str(result.device)


    client = Client(cluster)

    f = client.submit(test_gpu)
    f.result()

If successful, this should return ``(array(15., dtype=float32), '<CUDA Device 0>')``.

You can also verify that workers are using GPUs with the following command:

.. code-block:: python

    cluster.scheduler_info["workers"]
